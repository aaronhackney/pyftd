from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestFTDNetworkObjects(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    def test_crud_operations_network_objects(self):
        # Create
        net_obj = self.ftd_client.create_network_object(
            {"name": "TEST-NET", "subType": "NETWORK", "value": "10.1.1.0/24", "type": "networkobject"}
        )
        self.assertEqual(net_obj.name, "TEST-NET")

        fqdn_obj = self.ftd_client.create_network_object(
            {
                "name": "TEST-FQDN",
                "subType": "FQDN",
                "value": "www.example.com",
                "dnsResolution": "IPV4_AND_IPV6",
                "type": "networkobject",
            }
        )
        self.assertEqual(fqdn_obj.name, "TEST-FQDN")

        host_obj = self.ftd_client.create_network_object(
            {"name": "TEST-HOST", "subType": "HOST", "value": "10.1.1.1", "type": "networkobject"}
        )
        self.assertEqual(host_obj.name, "TEST-HOST")

        range_obj = self.ftd_client.create_network_object(
            {
                "name": "TEST-RANGE",
                "subType": "RANGE",
                "value": "10.0.0.1-10.0.0.100",
                "dnsResolution": "IPV4_AND_IPV6",
                "type": "networkobject",
            }
        )
        self.assertEqual(range_obj.name, "TEST-RANGE")

        # Read
        net_object_list = self.ftd_client.get_network_object_list(filter="name:TEST-NET")
        self.assertEqual(net_object_list[0].name, "TEST-NET")
        net_object = self.ftd_client.get_network_object(net_object_list[0].id)
        self.assertEqual(net_object_list[0], net_object)

        # Update
        host_obj.value = "192.168.0.1"
        updated_host_obj = self.ftd_client.edit_network_object(host_obj)
        self.assertEqual(updated_host_obj.value, "192.168.0.1")

        # Delete
        self.ftd_client.delete_network_object(updated_host_obj.id)
        self.ftd_client.delete_network_object(net_obj.id)
        self.ftd_client.delete_network_object(fqdn_obj.id)
        self.ftd_client.delete_network_object(range_obj.id)
        self.assertFalse(self.ftd_client.get_network_object_list(filter="name:TEST-NET"))
        self.assertFalse(self.ftd_client.get_network_object_list(filter="name:TEST-FQDN"))
        self.assertFalse(self.ftd_client.get_network_object_list(filter="name:TEST-HOST"))
        self.assertFalse(self.ftd_client.get_network_object_list(filter="name:TEST-RANGE"))

    def test_crud_operations_network_object_groups(self):
        # Create
        net_obj_1 = self.ftd_client.create_network_object(
            {"name": "TEST-123", "subType": "HOST", "value": "10.1.1.1", "type": "networkobject"}
        )
        net_obj_2 = self.ftd_client.get_network_object_list(filter="name:any-ipv4")
        network_objs = [net_obj_1, net_obj_2[0]]
        net_obj_grp = self.ftd_client.create_network_object_group(
            {
                "name": "Test-Group",
                "description": "Test Net obj Grp",
                "objects": network_objs,
                "type": "networkobjectgroup",
            }
        )

        # Read
        net_obj_group_list = self.ftd_client.get_network_object_group_list(filter="name:Test-Group")
        read_net_obj_grp = self.ftd_client.get_network_object_group(net_obj_group_list[0].id)
        self.assertEqual(len(read_net_obj_grp.objects), 2)

        # Update
        read_net_obj_grp.objects.pop(1)
        updated_net_obj_grp = self.ftd_client.edit_network_object_group(read_net_obj_grp)
        self.assertEqual(len(updated_net_obj_grp.objects), 1)

        # Delete
        self.ftd_client.delete_network_object_group(updated_net_obj_grp.id)
        self.assertFalse(self.ftd_client.get_network_object_group_list(filter="name:Test-Group"))
        self.ftd_client.delete_network_object(net_obj_1.id)
