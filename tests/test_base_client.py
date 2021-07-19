from unittest import TestCase
from pyftd import FTDClient
from os import environ, getcwd


class TestBaseCient(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        self.verify = True if environ.get("VERIFY") else False
        self.fdm_port = environ.get("FDMPORT") if environ.get("FDMPORT") else None
        self.proxies = environ.get("PROXIES") if environ.get("PROXIES") else None
        self.ftd_ip = environ.get("FTDIP")
        self.username = environ.get("FTDUSER")
        self.password = environ.get("FTDPASS")

    def test_get_api_version(self):
        self.assertTrue(
            FTDClient.get_api_version(self.ftd_ip, verify=self.verify, fdm_port=self.fdm_port, proxies=self.proxies)
        )

    def test_client_instance(self):
        self.ftd_client = FTDClient(
            self.ftd_ip,
            self.username,
            self.password,
            fdm_port=self.fdm_port,
            proxies=self.proxies,
            verify=self.verify,
        )
        self.assertIn("access_token", self.ftd_client.token)
