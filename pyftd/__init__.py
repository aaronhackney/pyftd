__version__ = "2.0.1"

import logging
from .base import FTDBaseClient
from .network_objects import FTDNetworkObjects
from .url_objects import FTDURLObjects
from .port_objects import FTDPortObjects
from .cert_objects import FTDCertificateObjects
from .secret_objects import FTDSecretObjects
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
    FTDCertificateObjects,
    FTDSecretObjects,
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

    Note that if an environment variable HTTP_PROXY=socks5://<proxyip>:<proxyport> exists, the client libraries will
    use this socks proxy by default and we do not have to expressly configure it in the constructor

    Sample usage:

    ftd_client = FTDClient(192.168.100.100, admin, "Admin123", verify=False)
    net_obj = ftd_client.create_network_object(
        {
            "name": "TEST-NET",
            "value": "10.1.1.0/24",
            "subType": "NETWORK",
            "type": "networkobject"
        }
    )
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
        """
        :param ftd_ip: str the ip address of the FTD device to be managed
        :param username: str an admin user
        :param password: str password for the admin-user (above)
        :param verify: bool verify the validity the SSL certificate or not (Hint, self-signed certs = FALSE)
        :param fdm_port: str (Optional) Used to connect to ftd on a port other than the standard port 443
        :type fdm_port: str (Optional) Soecify only if FDM is not listening on port 443
        :param proxies: dict (Optional) a dictionary of proxy servers like: proxies={"https": "socks5://127.0.0.1:9999"}
        """
        FTDBaseClient.__init__(self, ftd_ip, username, password, verify, fdm_port, proxies, timeout)
