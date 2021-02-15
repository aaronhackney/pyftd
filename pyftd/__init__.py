__version__ = "0.9.0"

import logging
from .base import FTDBaseClient
from .network_objects import FTDNetworkObjects
from .url_objects import FTDURLObjects
from .port_objects import FTDPortObjects
from typing import Optional

# from .ftd_backups import FTDBackups
# from .ftd_flex_config import FTDFlexConfig
# from .ftd_ha import FTDHighAvailability
# from .ftd_networking import FTDNetworking
# from .ftd_platform import FTDPlatform
# from .ftd_security_policy import FTDSecurityAccessPolicy
# from .ftd_feeds import FTDFeeds
# from .ftd_nat import FTDNat
# from .ftd_license import FTDLicense
# from .ftd_deployment import FTDDeploy

# from .ftd_anyconnect import FTDAnyConnect
# from .ftd_duo import FTDDUOConfig

log = logging.getLogger(__name__)


class FTDClient(
    FTDBaseClient,
    FTDNetworkObjects,
    FTDURLObjects,
    FTDPortObjects,
    # FTDBackups,
    # FTDFlexConfig,
    # FTDHighAvailability,
    # FTDNetworking,
    # FTDPlatform,
    # FTDSecurityAccessPolicy,
    # FTDDeploy,
    # FTDLicense,
    # FTDFeeds,
    # FTDNat,
    # FTDAnyConnect,
    # FTDDUOConfig,
):
    """The FTDClient is the primary interface that includes all of the API client libraries for FTD API (FDM)
    :param ftd_ip: the ip address of the FTD device to be managed
    :type ftd_ip: str
    :param verify: this determines if we should verify the validity the SSL certificate or not. (Hint, self-signed
    certificates will require this to be FALSE.
    :type verify: bool
    :param fdm_port: (Optional) Used If there is a need to jump through a proxy listening on an alternate port, other
    than the standard port 443
    :type fdm_port: str
    :param proxies: (Optional) a dictionary of proxy servers like: proxies={"https": "socks5://127.0.0.1:9999"}
    :type proxies: dict

    Note that if an environment variable HTTP_PROXY=socks5://<proxyip>:<proxyport> exists, the client libraries will
    use this socks proxy by default and we do not have to expressly configure it in the constructor

    All of the client classes are instantiated by simply instantiating the FTDClient class
    Sample usage:
    ftd_client = FTDClient('192.168.255.254', verify=False)
    ftd_client.get_access_token('my_username', 'my_password')
    ftd_client.swagger_client()
    ftd_client.add_tcp_port_object('my-port', '8443', 'My Port Object in FTD')
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
        FTDBaseClient.__init__(self, ftd_ip, username, password, verify, fdm_port, proxies, timeout)