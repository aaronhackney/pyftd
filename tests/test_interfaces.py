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