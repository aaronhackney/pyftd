from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestInterfafces(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    #############################
    # VRFs
    def test_crud_static_routes(self):
        # Read
        vrf_list = self.ftd_client.get_vrf_list()
        self.assertEqual(vrf_list[0].name, "Global")

        global_vrf = self.ftd_client.get_vrf(vrf_list[0].id)
        self.assertEqual(global_vrf.name, "Global")
