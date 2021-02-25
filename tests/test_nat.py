from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestNat(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)
        self.public_1 = self.ftd_client.create_network_object(
            {"name": "TEST-PUBLIC-1", "subType": "HOST", "value": "203.0.113.100", "type": "networkobject"}
        )
        self.public_2 = self.ftd_client.create_network_object(
            {"name": "TEST-PUBLIC-2", "subType": "HOST", "value": "203.0.113.200", "type": "networkobject"}
        )
        self.private_1 = self.ftd_client.create_network_object(
            {"name": "TEST-PRIVATE-1", "subType": "HOST", "value": "192.168.0.100", "type": "networkobject"}
        )
        self.private_2 = self.ftd_client.create_network_object(
            {"name": "TEST-PRIVATE-2", "subType": "HOST", "value": "192.168.0.200", "type": "networkobject"}
        )
        self.outside_int = self.ftd_client.get_physical_interface_list(filter="name~GigabitEthernet0/0")[0]
        self.inside_int = self.ftd_client.get_physical_interface_list(filter="name~GigabitEthernet0/1")[0]
        self.http_port = self.ftd_client.get_tcp_port_object_list(filter="name:HTTP")[0]
        self.https_port = self.ftd_client.get_tcp_port_object_list(filter="name:HTTPS")[0]

    def tearDown(self):
        self.ftd_client.delete_network_object(self.public_1.id)
        self.ftd_client.delete_network_object(self.public_2.id)
        self.ftd_client.delete_network_object(self.private_1.id)
        self.ftd_client.delete_network_object(self.private_2.id)

    def test_crud_operations_auto_nat(self):

        # Read auto-nat policy container
        nat_policy_container_list = self.ftd_client.get_autonat_container_list()
        nat_policy_container = self.ftd_client.get_autonat_container(nat_policy_container_list[0].id)

        # Create auto-nat
        auto_nat_policy = self.ftd_client.add_autonat_policy(
            nat_policy_container.id,
            {
                "type": "objectnatrule",
                "interfaceInTranslatedNetwork": False,
                "enabled": True,
                "description": "Test Auto Nat",
                "natType": "STATIC",
                "noProxyArp": True,
                "dns": True,
                "routeLookup": False,
                "name": "TEST-AUTO-NAT",
                "originalNetwork": self.private_1,
                "translatedNetwork": self.public_1,
                "sourceInterface": self.inside_int,
                "destinationInterface": self.outside_int,
            },
        )
        self.assertEqual(auto_nat_policy.name, "TEST-AUTO-NAT")

        # Read auto-nat
        self.assertEqual(
            self.ftd_client.get_autonat_policy(nat_policy_container.id, auto_nat_policy.id).id, auto_nat_policy.id
        )

        # Edit auto-nat
        auto_nat_policy.originalNetwork = self.private_2
        updated_auto_nat_policy = self.ftd_client.edit_autonat_policy(nat_policy_container.id, auto_nat_policy)
        self.assertEqual(updated_auto_nat_policy.originalNetwork.id, self.private_2.id)

        # Delete auto-nat
        self.ftd_client.delete_autonat_policy(nat_policy_container.id, updated_auto_nat_policy.id)
        self.assertFalse(self.ftd_client.get_autonat_policy_list(nat_policy_container.id, filter="fts~TEST-AUTO-NAT"))

    def test_crud_operations_manual_nat(self):
        # Read manual-nat policy container
        nat_policy_container_list = self.ftd_client.get_manual_nat_container_list()
        nat_policy_container = self.ftd_client.get_manual_nat_container(nat_policy_container_list[0].id)

        # Create manual-nat
        # Port foward port 443 on the outside interface self ip to private_1 on inside interface on port 80
        manual_nat_policy = self.ftd_client.add_manual_nat_policy(
            nat_policy_container.id,
            {
                "type": "manualnatrule",
                "interfaceInOriginalDestination": False,
                "interfaceInTranslatedSource": True,
                "enabled": True,
                "description": "Inbound Port forward outside_interface_ip:http to inside_host:443",
                "natType": "STATIC",
                "noProxyArp": True,
                "dns": False,
                "routeLookup": False,
                "name": "TEST-MANUAL-NAT",
                "originalSourcePort": self.http_port,
                "translatedSourcePort": self.https_port,
                "originalSource": self.private_1,
                "sourceInterface": self.inside_int,
                "destinationInterface": self.outside_int,
            },
        )
        self.assertEqual(manual_nat_policy.name, "TEST-MANUAL-NAT")

        # Update
        manual_nat_policy.originalSource = self.private_2
        updated_manual_nat_policy = self.ftd_client.edit_manual_nat_policy(nat_policy_container.id, manual_nat_policy)
        self.assertEqual(updated_manual_nat_policy.originalSource.id, self.private_2.id)

        # Delete
        self.ftd_client.delete_manual_nat_policy(nat_policy_container.id, updated_manual_nat_policy.id)
        self.assertFalse(
            self.ftd_client.get_manual_nat_policy_list(nat_policy_container.id, filter="fts~TEST-MANUAL-NAT")
        )
