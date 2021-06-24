from unittest import TestCase
from pyftd import FTDClient
from os import environ, path


class TestFTDNetworkObjects(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    FILENAME = "akh1.pcap"
    test = environ.get("FTDIP")

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    def test_download_disk_file(self):
        file = self.ftd_client.download_disk_file(self.FILENAME)
        self.assertIsNotNone(file)
        print(path.expanduser("~"))
        with open(f"{path.expanduser('~')}/{self.FILENAME}", "wb") as download_file:
            download_file.write(file)
        print("")
