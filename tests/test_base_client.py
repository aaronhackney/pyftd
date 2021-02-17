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
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    def test_get_api_version(self):
        self.assertTrue(FTDClient.get_api_version(environ.get("FTDIP"), verify=False))