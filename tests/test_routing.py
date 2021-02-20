from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestRouting(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)
        self.network_1 = self.ftd_client.create_network_object(
            {"name": "TEST-NET-1", "subType": "NETWORK", "value": "10.1.0.0/16", "type": "networkobject"}
        )
        self.network_2 = self.ftd_client.create_network_object(
            {"name": "TEST-NET-2", "subType": "NETWORK", "value": "192.168.0.0/24", "type": "networkobject"}
        )

        self.next_hop_1 = self.ftd_client.create_network_object(
            {"name": "TEST-NEXT-HOP-1", "subType": "HOST", "value": "172.30.0.254", "type": "networkobject"}
        )

        self.next_hop_2 = self.ftd_client.create_network_object(
            {"name": "TEST-NEXT-HOP-2", "subType": "HOST", "value": "10.255.255.254", "type": "networkobject"}
        )
        self.outside_int = self.ftd_client.get_physical_interface_list(filter="name~GigabitEthernet0/0")[0]

    def tearDown(self):
        self.ftd_client.delete_network_object(self.network_1.id)
        self.ftd_client.delete_network_object(self.network_2.id)
        self.ftd_client.delete_network_object(self.next_hop_1.id)
        self.ftd_client.delete_network_object(self.next_hop_2.id)

    #############################
    # VRFs
    def test_crud_vrf(self):
        # Read
        vrf_list = self.ftd_client.get_vrf_list()
        self.assertEqual(vrf_list[0].name, "Global")

        global_vrf = self.ftd_client.get_vrf(vrf_list[0].id)
        self.assertEqual(global_vrf.name, "Global")

    #############################
    # Static Routes
    def test_crud_static_routes(self):
        # Create
        route_obj = self.ftd_client.create_static_route(
            {
                "description": "test adding static route",
                "metricValue": 1,
                "ipType": "IPv4",
                "type": "staticrouteentry",
                "name": "unittest-route",
                "networks": [self.network_1],
                "gateway": self.next_hop_1,
                "iface": self.outside_int,
            }
        )
        self.assertEqual(route_obj.name, "unittest-route")

        # Read
        self.assertEqual(self.ftd_client.get_static_route_list(filter="name:unittest-route")[0].id, route_obj.id)

        # Update
        route_obj.metricValue = 3
        updated_static_route = self.ftd_client.edit_static_route(route_obj)
        self.assertEqual(updated_static_route.metricValue, 3)

        # delete
        self.ftd_client.delete_static_route(updated_static_route.id)
        self.assertFalse(self.ftd_client.get_static_route_list(filter="name:unittest-route"))
