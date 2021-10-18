from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestDHCP(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    def test_get_operations_dhcp_relay_services(self):
        dhcp_relay_services = self.ftd_client.get_dhcp_relay_services()
        self.assertIsNotNone(dhcp_relay_services)

        self.assertIsNotNone(self.ftd_client.get_dhcp_relay_service(dhcp_relay_services[0].id))

    def test_update_operations_dhcp_relay_services(self):
        # Test assumes that there is a physical interface called "inside" where the DCHP server resides
        # Test assumes that there is a physical interface called "dmz" where the dhcp clients reside
        # Test assumes that DHCP Server is not enabled on any interface where dhcp relay is to be set or we get a validation error
        # 422 Unprocessable Entity
        # "DHCP Relay Service cannot be enabled if the DHCP Server feature is also enabled on any interface."

        # Create DHCP Server network object
        test_dhcp_server = self.ftd_client.create_network_object(
            {
                "name": "test-dhcp-server",
                "description": "Test DHCP Server Object",
                "subType": "HOST",
                "value": "192.168.45.100",
                "type": "networkobject",
            }
        )

        # Get existing dhcp relay services
        dhcp_relay_service = self.ftd_client.get_dhcp_relay_services()[0]

        # Edit existing dhcp relay services
        dhcp_relay_service.servers = [
            {
                "server": self.ftd_client.get_network_object_list(filter="name:test-dhcp-server")[0],
                "interface": self.ftd_client.get_physical_interface_list(filter="name:inside")[0],
                "type": "dhcprelayserver",
            }
        ]
        dhcp_relay_service.agents = [
            {
                "enableIpv4Relay": True,
                "setRoute": True,
                "interface": self.ftd_client.get_physical_interface_list(filter="name:dmz")[0],
                "type": "dhcprelayagent",
            }
        ]

        # Update the dhcp relay settings
        updated_dhcp_relay_service = self.ftd_client.update_dhcp_relay_service(dhcp_relay_service)
        self.assertTrue(dhcp_relay_service.servers)
        self.assertTrue(dhcp_relay_service.agents)

        # Remove our dhcp relay settings
        updated_dhcp_relay_service.servers = []
        updated_dhcp_relay_service.agents = []

        # Verify we have removed the servers and agents for DHCP relay
        deleted_dhcp_relay_settings = self.ftd_client.update_dhcp_relay_service(updated_dhcp_relay_service)
        self.assertIsNone(deleted_dhcp_relay_settings.servers)
        self.assertIsNone(deleted_dhcp_relay_settings.agents)

        # Delete dhcp host
        self.ftd_client.delete_network_object(test_dhcp_server.id)
