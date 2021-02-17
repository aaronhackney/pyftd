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

    def test_crud_operations_url_object(self):
        # Create
        url_obj = self.ftd_client.create_url_object(
            {"url": "www.example.com", "description": "test url object", "type": "urlobject", "name": "test-url"}
        )
        self.assertEqual(self.ftd_client.get_url_object_list(filter="name:test-url")[0].id, url_obj.id)

        # Read
        self.assertEqual(self.ftd_client.get_url_object(url_obj.id), url_obj)

        # Update
        url_obj.name = "new-test-url"
        updated_url_obj = self.ftd_client.edit_url_object(url_obj)
        self.assertEqual(updated_url_obj.name, "new-test-url")

        # Delete
        self.ftd_client.delete_url_object(updated_url_obj.id)
        self.assertFalse(self.ftd_client.get_url_object_list(filter="name:new-test-url"))

    def test_crud_operations_url_grp_object(self):
        # Create
        url_obj_1 = self.ftd_client.create_url_object(
            {"url": "www.example1.com", "description": "test url object 1", "type": "urlobject", "name": "test-url-1"}
        )
        url_obj_2 = self.ftd_client.create_url_object(
            {"url": "www.example2.com", "description": "test url object 2", "type": "urlobject", "name": "test-url-2"}
        )
        url_grp_obj = self.ftd_client.create_url_object_group(
            {
                "name": "Test-URL-GRP",
                "description": "Testing URL Group",
                "objects": [url_obj_1, url_obj_2],
                "type": "urlobjectgroup",
            }
        )
        self.assertEqual(url_grp_obj.name, "Test-URL-GRP")

        # Read
        self.assertEqual(self.ftd_client.get_url_object_group(url_grp_obj.id), url_grp_obj)

        # Update
        url_grp_obj.name = "Updated-Test-URL-GRP"
        updated_url_group = self.ftd_client.edit_url_object_group(url_grp_obj)
        self.assertEqual(updated_url_group.name, "Updated-Test-URL-GRP")

        # Delete
        self.ftd_client.delete_url_object_group(updated_url_group.id)
        self.assertFalse(self.ftd_client.get_url_object_group_list(filter="name:Updated-Test-URL-GRP"))
        self.ftd_client.delete_url_object(url_obj_1.id)
        self.ftd_client.delete_url_object(url_obj_2.id)
