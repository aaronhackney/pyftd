from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestFTDIdentityObjects(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    def test_crud_operations_Radius_identity_objects(self):
        # Create
        radius_ident_obj = self.ftd_client.create_radius_identity_source(
            {
                "name": "MY_RADIUS_10.10.10.111",
                "description": "Radius server at 10.10.10.111",
                "host": "10.10.10.111",
                "capabilities": ["AUTHENTICATION", "AUTHORIZATION"],
                "timeout": 2,
                "serverAuthenticationPort": 1812,
                "serverSecretKey": "abc123",
                "useRoutingToSelectInterface": True,
                "type": "radiusidentitysource",
            }
        )
        self.assertEqual(radius_ident_obj.host, "10.10.10.111")

        # Read
        self.assertEqual(self.ftd_client.get_radius_identity_source(radius_ident_obj.id).id, radius_ident_obj.id)

        # Update
        radius_ident_obj.host = "192.168.0.111"
        updated_radius_ident_obj = self.ftd_client.edit_radius_identity_source(radius_ident_obj)
        self.assertTrue(updated_radius_ident_obj.host, "192.168.0.111")

        # Delete
        self.ftd_client.delete_radius_identity_source(updated_radius_ident_obj.id)
        self.assertFalse(self.ftd_client.get_radius_identity_source_list(filter="name:MY_RADIUS_10.10.10.111"))

    def test_crud_operations_radius_identity_source_groups(self):
        # Create Radius objects to add to the group for group testing
        radius_ident_obj_1 = self.ftd_client.create_radius_identity_source(
            {
                "name": "MY_RADIUS_10.10.10.111",
                "description": "Radius server at 10.10.10.111",
                "host": "10.10.10.111",
                "capabilities": ["AUTHENTICATION", "AUTHORIZATION"],
                "timeout": 2,
                "serverAuthenticationPort": 1812,
                "serverSecretKey": "abc123",
                "useRoutingToSelectInterface": True,
                "type": "radiusidentitysource",
            }
        )

        radius_ident_obj_2 = self.ftd_client.create_radius_identity_source(
            {
                "name": "MY_RADIUS_10.10.10.112",
                "description": "Radius server at 10.10.10.112",
                "host": "10.10.10.112",
                "capabilities": ["AUTHENTICATION", "AUTHORIZATION"],
                "timeout": 2,
                "serverAuthenticationPort": 1812,
                "serverSecretKey": "abc123",
                "useRoutingToSelectInterface": True,
                "type": "radiusidentitysource",
            }
        )

        # Create
        radius_identity_src_grp = self.ftd_client.create_radius_identity_source_group(
            {
                "name": "MYRADIUSGRP",
                "description": "MY RADIUS GROUP",
                "deadTime": 5,
                "maxFailedAttempts": 3,
                "radiusIdentitySources": [radius_ident_obj_1, radius_ident_obj_2],
                "type": "radiusidentitysourcegroup",
            }
        )

        # Read
        self.assertEqual(
            self.ftd_client.get_radius_identity_source_group(radius_identity_src_grp.id).id, radius_identity_src_grp.id
        )

        # Update
        radius_identity_src_grp.radiusIdentitySources = [radius_ident_obj_1]
        updated_radius_identity_src_grp = self.ftd_client.edit_radius_identity_source_group(radius_identity_src_grp)
        self.assertEqual(
            len(self.ftd_client.get_radius_identity_source_group(radius_identity_src_grp.id).radiusIdentitySources), 1
        )

        # Delete
        self.ftd_client.delete_radius_identity_source_group(updated_radius_identity_src_grp.id)
        self.assertFalse(self.ftd_client.get_radius_identity_source_group_list(filter="name:MYRADIUSGRP"))
        self.ftd_client.delete_radius_identity_source(radius_ident_obj_1.id)
        self.ftd_client.delete_radius_identity_source(radius_ident_obj_2.id)