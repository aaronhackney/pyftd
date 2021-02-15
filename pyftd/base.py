import logging
import sys
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from bravado.exception import HTTPUnauthorized, HTTPForbidden, HTTPUnprocessableEntity, HTTPLocked
from bravado_core.exception import SwaggerMappingError
from typing import Optional, Union
from requests import Session
from functools import wraps
from time import sleep
from json import loads
import requests

logger = logging.getLogger(__name__)


class FTDAPIWrapper(object):
    """This decorator class wraps all API methods of ths client and solves a number of issues.

    1. HTTPUnauthorized: If the token comes back as invalid, presumably due to expiration, the wrapper will obtain a new
    token and retry the original API call.

    2. HTTPForbidden: If the setup wizard has never been run, catch that condition with a HTTPForbidden error, bypass
    the startup wizard and obtain an evaluation base license for the ftd. This removes the need for a script to check
    for this condition before making api calls.

    3. HTTPUnprocessableEntity: If someone tries to create an object that already exists, catch the error with
    HTTPUnprocessableEntity, report the error via the logger and move on. If the HTTPUnprocessableEntity error was not a
    duplicate object error, provide a little more detail to the error logger, like the name of the method that made the
    original call.

    4. SwaggerMappingError: Catch the SwaggerMappingError and  provide a little more detail to the error logger, like
    the name of the method that made the original call and then re-throw the SwaggerMappingError.

    5. HTTPLocked: Occasionally, the database becomes locked due to heavy operations like vulnerability updates or SI
    update. This catches a database lock error, waits 10 seconds for the lock to cear and then retires the original
    call. If the DB is still locked, this will throw "an exception while handling an exception" error and the call will
    fail.
    """

    def __call__(self, fn):
        # TODO: Add HA check here....
        @wraps(fn)
        def new_func(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except HTTPUnauthorized as ex:
                logger.error(f"FTDAPIWrapper called by {fn.__name__}, but our token appears to be invalid: {ex}")
                logger.error("Attempting to obtain a new token...")
                args[0].get_access_token()  # Update the token in our objects
                args[0].get_swagger_client()  # swagger_client has a copy of the token, so update it too!
                logger.warning(f"New token acquired. Now executing the original call to {fn.__name__}")
                return fn(*args, **kwargs)
            except HTTPForbidden as ex:
                if not args[0].is_setup_wizard():
                    logger.warning(
                        f"{fn.__name__} was called but the setup wizard has yet not been executed. "
                        f"We will attempt to skip the setup wizard and activate an evaluation base license."
                    )
                    args[0].skip_setup_wizard()
                    logger.warning("Setup wizard and licensing stage appears to have been successful.")
                    logger.warning(f"Executing the original call to {fn.__name__}")
                    return fn(*args, **kwargs)
                else:
                    logger.error(f"There is a problem accessing the FTD's API: {ex}")
                    raise HTTPForbidden
            except HTTPUnprocessableEntity as ex:
                for message in ex.swagger_result.error.messages:
                    if message.code in [
                        "duplicateName",
                        "duplicateSyslogServerIPAddressAndPortNumber",
                        "manualNatDuplicateRule",
                        "objectNatDupRuleWithSameOrigNetwork",
                    ]:
                        logger.error(f"{message.description} Skipping...")
                        return
                    if message.description == "Failed to schedule deployment job":
                        logger.error("We failed to schedule the deployment job. Waiting 10 seconds and then retrying.")
                        sleep(10)
                        return fn(*args, **kwargs)
                logger.error(f"FTDAPIWrapper called by {fn.__name__}, but we got an error: {ex}")
                logger.debug({sys.exc_info()[0]})
                raise HTTPUnprocessableEntity
            except SwaggerMappingError as ex:
                logger.error(f"FTDAPIWrapper called by {fn.__name__}, but we got an error: {ex}")
                logger.error({sys.exc_info()[0]})
                raise SwaggerMappingError
            except HTTPLocked as ex:
                logger.error("We got a database locked response from the API. Waiting 10 seconds and then retrying.")
                sleep(10)
                return fn(*args, **kwargs)

        return new_func


class FTDBaseClient(object):
    """
    This class is inherited by all FTD API classes and is always instantiated and is where the auth token for the FTD
    is obtained and other functions that are needed by multiple inherited classes

    Note that if an environment variable HTTP_PROXY=socks5://<proxyip>:<proxyport> exists, the client libraries will
    use this socks proxy by default and we do not have to expressly configure it in the constructor
    """

    def __init__(
        self,
        ftd_ip: str,
        username: str,
        password: str,
        verify: bool = True,
        fdm_port: Optional[str] = None,
        proxies: Optional[dict] = None,
        timeout: int = 30,
    ):
        self.proxies = proxies
        self.fdm_port = str(fdm_port)
        self.base_url = f"https://{ftd_ip}:{self.fdm_port}" if fdm_port else f"https://{ftd_ip}"
        self.verify = verify  # allow API self-signed certs * DANGER *
        self.common_prefix = f"{self.base_url}/api/fdm/latest"
        self.swagger_client = None
        self.ha_role = None  # SINGLE_NODE, HA_PRIMARY, or HA_SECONDARY
        self.verify = verify
        self.http_session = Session()
        self.http_session.proxies = proxies
        self.username = username
        self.password = password
        self.token = None
        self.timeout = timeout

    def get_api_version(self) -> Union[dict, None]:
        """
        This is callable without authentication and without instantiation the swagger client to get the API version.
        The API version is a hint at the major code version running on the box. Note that knowing the version is not
        mandatory, for example, we can always use '/api/fdm/latest' vs '/api/fdm/v4' when making API calls.
        :return: api version
        """
        api_response = self.http_session.get(
            url=self.base_url + "/api/versions", verify=self.verify, timeout=self.timeout
        )
        data = api_response.json()
        if "supportedVersions" in data:
            return data["supportedVersions"][0]

    def get_access_token(self) -> Union[dict, None]:
        """
        :param timeout: wait this many seconds before declaring the device unreachable
        :return:    If successful: None - simply add the bearer token to the object and move on
                    Else:   return the API response so that the client consumer might capture the error and handle
        """
        # TODO: Handle 503 responses from the FTD (Booting or manager on-boxing not yet complete)
        # Remove existing token if there is one stored in the request object
        if "Authorization" in self.http_session.headers:
            del self.http_session.headers["Authorization"]
            logger.debug("Existing Authorization token found. Deleting...")

        auth_payload = {"grant_type": "password", "username": self.username, "password": self.password}

        # Auth to FTD and retrieve a bearer token and update the headers in the request object with the auth header
        api_response = self.http_session.post(
            self.common_prefix + "/fdm/token", json=auth_payload, verify=self.verify, timeout=self.timeout
        )
        if api_response is not None and 200 <= api_response.status_code <= 299:
            self.http_session.headers.update({"Authorization": f"Bearer {api_response.json()['access_token']}"})
            self.token = api_response.json()
            logger.debug("Token successfully acquired")
        else:
            logger.error(
                "We failed to successfully acquire a token from the FTD. Check your credentials and try again."
            )
            return api_response

    def post(
        self,
        endpoint: str,
        post_data: Optional[dict] = None,
        file_path: str = None,
        headers: Optional[dict] = None,
    ) -> dict:
        """
        Mainly used for things not covered by the swagger API. such as uploading files to the devices.
        :param endpoint: The fqdn + path of the API we are hitting
        :param post_data: post data, if any
        :param file_path: The path to the file we are uploading
        :param headers: Any additional headers needed
        :return: request response
        """
        if headers is None:  # Allows us to override obj headers
            headers = self.http_session.headers
        try:
            if file_path:  # Handle file uploads
                files = {"fileToUpload": open(file_path, "rb")}
            else:
                files = None
            response = requests.post(
                self.common_prefix + endpoint,
                headers=headers,
                json=post_data,
                files=files,
                verify=self.verify,
                timeout=self.timeout,
            )
            if response.content:
                payload = loads(response.content.decode("utf-8"))
            else:
                payload = dict()
            return payload
        except FileNotFoundError as e:
            logger.error(e)
            return {"status_code": 500}

    def logout(self) -> Union[dict, None]:
        """This call will invalidate a token"""
        logout_payload = {
            "grant_type": "revoke_token",
            "access_token": self.token["access_token"],
            "token_to_revoke": self.token["access_token"],
        }
        api_response = self.http_session.post(
            self.common_prefix + "/fdm/token", json=logout_payload, verify=self.verify, timeout=self.timeout
        )
        if api_response is not None and 200 <= api_response.status_code <= 299:
            logger.warning("Logout Successful. Your API token is no longer valid.")
            # We are not going to remove the token from this object or the session headers. This call is mostly
            # used for testing our 401 decorator
        else:
            logger.error("We failed to successfully Log out of the FTD.")
            return api_response

    def get_swagger_client(self) -> None:
        """From here on out, most of the API calls to the FTD will be swagger calls through the bravado client instead
        of using the standard Requests library. We use our extended class ExtendedRequestsClient which extends the
        bravado RequestsClient and give us an opportunity to add proxy support"""
        bravado_req_client = ExtendedRequestsClient(proxies=self.proxies)
        bravado_req_client.session.trust_env = self.verify
        bravado_req_client.ssl_verify = self.verify

        if "Authorization" not in self.http_session.headers:
            logger.error("swagger_client was called but no auth token was passed!")
            raise ValueError

        # Copy the session headers to the bravado client for authentication
        bravado_req_client.session.headers = self.http_session.headers.copy()

        self.swagger_client = SwaggerClient.from_url(
            self.base_url + "/apispec/ngfw.json",
            http_client=bravado_req_client,
            config={"validate_responses": False, "validate_swagger_spec": False},
        )

    @FTDAPIWrapper()
    def skip_setup_wizard(self) -> None:
        """If the setup wizard has not been run or skipped, we cannot configure the device with API calls. Skip the
        setup wizard and enable the trial licensing. This is not in the swagger_client SPEC file so we will have to do
        this the old fashioned way with direct Requests library calls."""

        # Step 1: Set the license to evaluation mode
        payload = {"token": None, "connectionType": "EVALUATION", "type": "smartagentconnection", "version": None}
        self.http_session.post(
            self.common_prefix + "/license/smartagentconnections",
            json=payload,
            verify=self.verify,
            timeout=self.timeout,
        )

        # Step 2:Skip the setup-wizard in the GUI
        payload = {
            "taskComplete": True,
            "nextPage": None,
            "currentPage": None,
            "type": "easysetupstatus",
            "version": None,
        }
        self.http_session.post(self.common_prefix + "/easysetup/easysetupstatus", json=payload, verify=self.verify)

    @FTDAPIWrapper()
    def is_setup_wizard(self) -> bool:
        """Before we attempt to configure the device, we need to know if we are in a first-boot situation. Check to see
        if the platform is still displaying the setup wizard or if the setup wizard has been skipped. This is not in
        the swagger_client SPEC file so we will have to do this the old fashioned way.
        :return: True if the setup wizard has been run and completed, false if we still need to run/bypass the wizard
        :rtype: bool"""
        api_response = self.http_session.get(
            url=self.common_prefix + "/easysetup/easysetupstatus", verify=self.verify, timeout=self.timeout
        )
        if api_response.status_code == 403:
            return False
        elif api_response.status_code == 200:
            return True

    @FTDAPIWrapper()
    def run_cli_command(self, command: str) -> Union[dict, None]:
        """
        Given a cli command, return the cli response of the command
        :param command: string of the cli command we wish to run and receive output from
        :return:
        """
        # TODO move this to a cli class with other common cli tasks
        body = {"commandInput": command, "type": "Command"}
        res = self.swagger_client.Command.addCommand(body=body).result()
        if res:
            return res.commandOutput


class ExtendedRequestsClient(RequestsClient):
    """This extends the bravado requests client to add proxy support"""

    def __init__(self, proxies: Optional[dict] = None) -> None:
        super(ExtendedRequestsClient, self).__init__()
        if proxies is not None:
            self.session.proxies.update(proxies)
