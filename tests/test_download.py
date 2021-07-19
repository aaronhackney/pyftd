from unittest import TestCase
from pyftd import FTDClient
from os import environ, path, remove


class TestFTDNetworkObjects(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables CAP_FILENAME, FTDIP, FTDUSER, and FTDPASS
    Optional bash variables include VERIFY, PROXIES and FDMPORT
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    FILENAME = environ.get("CAP_FILENAME")

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(
            environ.get("FTDIP"),
            environ.get("FTDUSER"),
            environ.get("FTDPASS"),
            fdm_port=environ.get("FDMPORT"),
            proxies=environ.get("PROXIES"),
            verify=verify,
        )

    def test_download_disk_file(self):
        self.remove_test_file()  # make sure the capture isn't already on disk
        file = self.ftd_client.download_disk_file(self.FILENAME)
        self.assertIsNotNone(file)
        print(path.expanduser("~"))
        with open(f"{path.expanduser('~')}/{self.FILENAME}", "wb") as download_file:
            download_file.write(file)
        self.assertTrue(path.exists(f"{path.expanduser('~')}/{self.FILENAME}"))
        self.remove_test_file()  # clean up by removing the capture

    def remove_test_file(self):
        if path.exists(f"{path.expanduser('~')}/{self.FILENAME}"):
            remove(f"{path.expanduser('~')}/{self.FILENAME}")
