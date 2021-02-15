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
        self.ftd_client.get_access_token()
        self.ftd_client.get_swagger_client()

    #############################
    # TCP Port Objects
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

    #############################
    # UDP Port Objects
    def test_crud_operations_udp_port_objects(self):
        # create
        udp_port_obj = self.ftd_client.create_udp_port_object(
            {"name": "UDP-Port-Test", "description": "test", "port": "25", "type": "udpportobject"}
        )
        self.assertTrue(udp_port_obj.name, "UDP-Port-Test")

        # Read
        self.assertTrue(self.ftd_client.get_udp_port_object(udp_port_obj.id), udp_port_obj)

        # Update
        udp_port_obj.port = "26"
        updated_udp_port_obj = self.ftd_client.edit_udp_port_object(udp_port_obj)
        self.assertTrue(updated_udp_port_obj.port, "26")

        # Delete
        self.ftd_client.delete_udp_port_object(updated_udp_port_obj.id)
        self.assertFalse(self.ftd_client.get_udp_port_object_list(filter="name:UDP-Port-Test"))

    #############################
    # ICMP Port Objects
    def test_crud_operations_ipv4_icmp_objects(self):
        # create
        icmp_obj = self.ftd_client.create_ipv4_icmp_port_object(
            {
                "name": "ICMP_TEST",
                "icmpv4Type": "ECHO_REPLY",
                "type": "icmpv4portobject",
                "description": "Unittest ipv4 icmp",
            }
        )

        # Read
        self.assertEqual(self.ftd_client.get_ipv4_icmp_port_object(icmp_obj.id), icmp_obj)

        # Update
        icmp_obj.icmpv4Type = "ECHO_REQUEST"
        updated_icmp_obj = self.ftd_client.edit_ipv4_icmp_port_object(icmp_obj)
        self.assertEqual(updated_icmp_obj.icmpv4Type, "ECHO_REQUEST")

        # Delete
        self.ftd_client.delete_ipv4_icmp_port_object(icmp_obj.id)
        self.assertFalse(self.ftd_client.get_ipv4_icmp_port_object_list(filter="name:ICMP_TEST"))

    def test_crud_operations_port_object_groups(self):
        # create
        port_obj_1 = self.ftd_client.create_tcp_port_object(
            {"name": "TCP-Port-Test", "description": "test", "port": "25", "type": "tcpportobject"}
        )
        port_obj_2 = self.ftd_client.create_udp_port_object(
            {"name": "UDP-Port-Test", "description": "test", "port": "25", "type": "udpportobject"}
        )
        port_obj_grp = self.ftd_client.create_port_object_group(
            {
                "name": "Test-Port-Grp",
                "description": "Test creating a port group",
                "objects": [port_obj_1, port_obj_2],
                "type": "portobjectgroup",
            }
        )
        self.assertEqual(len(port_obj_grp.objects), 2)

        # Read
        self.assertEqual(self.ftd_client.get_port_object_group(port_obj_grp.id), port_obj_grp)
        self.assertTrue(self.ftd_client.get_port_object_group_list(filter="name:Test-Port-Grp"))

        # Change
        port_obj_grp.name = "Updated-Test-Port-Grp"
        updated_port_obj_grp = self.ftd_client.edit_port_object_group(port_obj_grp)
        self.assertEqual(updated_port_obj_grp.name, "Updated-Test-Port-Grp")

        # Delete
        self.ftd_client.delete_port_object_group(updated_port_obj_grp.id)
        self.assertFalse(self.ftd_client.get_port_object_group_list(filter="name:Updated-Test-Port-Grp"))
        self.ftd_client.delete_tcp_port_object(port_obj_1.id)
        self.ftd_client.delete_udp_port_object(port_obj_2.id)
