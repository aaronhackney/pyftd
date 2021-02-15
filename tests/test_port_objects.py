from unittest import TestCase
from pyftd import FTDClient
from random import randint
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
        self.ftd_client.get_access_token()
        self.ftd_client.get_swagger_client()

    def test_crud_operations_tcp_port_objects(self):
        # create
        tcp_port_obj = self.ftd_client.create_tcp_port_object(
            {"name": "TCP-Port-Test", "description": "test", "port": "25", "type": "tcpportobject"}
        )
        self.assertTrue(tcp_port_obj.name, "TCP-Port-Test")

        # Read
        self.assertTrue(self.ftd_client.get_tcp_port_object(tcp_port_obj.id), tcp_port_obj)

        # Update
        tcp_port_obj.port = "26"
        updated_tcp_port_obj = self.ftd_client.edit_tcp_port_object(tcp_port_obj)
        self.assertTrue(updated_tcp_port_obj.port, "26")

        # Delete
        self.ftd_client.delete_tcp_port_object(updated_tcp_port_obj.id)
        self.assertFalse(self.ftd_client.get_tcp_port_object_list(filter="name:TCP-Port-Test"))

        # UDP NEXT