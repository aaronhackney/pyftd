from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestURLObjects(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    def test_crud_operations_secret_objects(self):
        # Create
        secret_obj = self.ftd_client.create_secret_object(
            {
                "name": "TEST_TACACS_PSK",
                "password": "abc123",
                "description": "FTD TACACS+ PSK",
                "type": "secret",
            }
        )
        self.assertEqual(secret_obj.name, "TEST_TACACS_PSK")

        # Read
        self.assertEqual(self.ftd_client.get_secret_object(secret_obj.id).id, secret_obj.id)

        # Update
        secret_obj.password = "password1"
        updated_secret_obj = self.ftd_client.edit_secret_object(secret_obj)
        self.assertEqual(updated_secret_obj.name, "TEST_TACACS_PSK")

        # Delete
        self.ftd_client.delete_secret_object(secret_obj.id)
        self.assertFalse(self.ftd_client.get_secret_object_list(filter="name:TEST_TACACS_PSK"))
