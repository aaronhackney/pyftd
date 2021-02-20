from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestInterfafces(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    #############################
    # Physical Interface Objects
    def test_crud_operations_physical_interfaces(self):
        # Create
        # We cannot create a physical interface...they just exist...

        # Read
        interface_list = self.ftd_client.get_physical_interface_list()
        self.assertTrue(interface_list)
        interface_obj = self.ftd_client.get_physical_interface(interface_list[2].id)
        self.assertIn("Ethernet", interface_obj.hardwareName)

        # Update
        interface_obj.name = "dmz"
        interface_obj.description = "DMZ Danger Zone"
        interface_obj.duplexType = "AUTO"
        interface_obj.speedType = "AUTO"
        interface_obj.mode = "ROUTED"
        interface_obj.security = 100
        interface_obj.enabled = True
        interface_obj.ipv4 = {
            "ipType": "STATIC",
            "type": "interfaceipv4",
            "ipAddress": {
                "standbyIpAddress": "192.168.200.2",
                "type": "haipv4address",
                "netmask": "255.255.255.0",
                "ipAddress": "192.168.200.1",
            },
        }
        updated_interface = self.ftd_client.edit_physical_interface(interface_obj)
        self.assertEqual(updated_interface.ipv4.ipAddress.ipAddress, "192.168.200.1")

        # Delete
        # Physical interfaces cannot be deleted

    #############################
    # SubInterfaces Interface Objects
    def test_crud_operations_sub_interfaces(self):
        phys_int_list = self.ftd_client.get_physical_interface_list()
        # Create
        sub_int = self.ftd_client.create_sub_interface(
            phys_int_list[2].id,
            {
                "type": "subinterface",
                "subIntfId": 109,
                "vlanId": 109,
                "mtu": 1500,
                "mode": "ROUTED",
                "present": True,
                "security": 0,
                "enabled": True,
                "hardwareName": "GigabitEthernet0/0.101",
                "description": "VLAN 101 Sub Interface",
                "monitorInterface": True,
                "ipv4": {
                    "ipType": "STATIC",
                    "dhcpRouteMetric": 1,
                    "defaultRouteUsingDHCP": True,
                    "type": "interfaceipv4",
                    "ipAddress": {
                        "standbyIpAddress": "",
                        "type": "haipv4address",
                        "netmask": "255.255.255.0",
                        "ipAddress": "172.16.16.254",
                    },
                },
                "name": "uat",
            },
        )
        self.assertEqual(sub_int.vlanId, 109)

        # Update
        sub_int.vlanId = 901
        updated_sub_int = self.ftd_client.update_sub_interface(phys_int_list[2].id, sub_int)
        self.assertEqual(updated_sub_int.vlanId, 901)

        # Read
        self.assertEqual(self.ftd_client.get_sub_interface(phys_int_list[2].id, sub_int.id).id, sub_int.id)

        # Delete
        self.ftd_client.delete_sub_interface(phys_int_list[2].id, sub_int.id)

    #############################
    # Interfaces Operational Status and Info
    def test_interface_operational_status(self):
        int_status_list = self.ftd_client.get_interface_operational_status_list()
        self.assertTrue(int_status_list)
        int_status = self.ftd_client.get_interface_operational_status(int_status_list[2].id)
        self.assertIn(int_status.linkState, ["UP", "DOWN"])

    def test_get_interface_info_list(self):
        int_info_list = self.ftd_client.get_interface_info_list()
        self.assertTrue(int_info_list)
