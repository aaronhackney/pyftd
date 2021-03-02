from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestPlatform(TestCase):
    """
    These test run against an actual FTD device.
    Set your FTP IP, Username and password using bash variables FTDIP, FTDUSER, and FTDPASS
    Note: If you want to enable TLS certificate verification, add VERIFY=True to your .env or env varaibles
          If you do not want to enable TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        verify = True if environ.get("VERIFY") else False
        self.ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)
        self.dns_group_test = self.ftd_client.create_dnsgroup_object(
            {
                "name": "My-Umbrella-Ella-Ella",
                "dnsServers": [
                    {"ipAddress": "208.67.222.222", "type": "dnsserver"},
                    {"ipAddress": "208.67.220.220", "type": "dnsserver"},
                ],
                "timeout": 2,
                "retries": 2,
                "searchDomain": "hacksbrain.com",
                "type": "dnsservergroup",
            }
        )

    def tearDown(self):
        self.ftd_client.delete_dnsgroup_object(self.dns_group_test.id)

    def test_get_system_information(self):
        # Read - Read is the only operation for system information
        sys_info = self.ftd_client.get_system_information()
        self.assertTrue(sys_info.softwareVersion)

    def test_crud_operations_hostname(self):
        # Create - No create operation - the hostname always exists

        # Read
        hostname_list = self.ftd_client.get_hostname_list()
        self.assertTrue(hostname_list)

        hostname = self.ftd_client.get_hostname(hostname_list[0].id)
        self.assertTrue(hostname.hostname)

        # Update
        hostname.hostname = "MyFTD" if hostname.hostname != "MyFTD" else "MyFTD-TEST"
        updated_hostname = self.ftd_client.edit_hostname(hostname)
        self.assertIn(updated_hostname.hostname, ["MyFTD", "MyFTD-TEST"])

        # Delete - No delete operation - the hostname always exists

    def test_crud_operations_management_dns(self):
        # Create - There are no create APIs - DNS settings always exist

        # Read
        mgmt_dns_server_settings_list = self.ftd_client.get_mgmt_dns_settings_list()
        self.assertTrue(mgmt_dns_server_settings_list)
        mgmt_dns_server_settings = self.ftd_client.get_mgmt_dns_settings(mgmt_dns_server_settings_list[0].id)
        self.assertEqual(mgmt_dns_server_settings.id, mgmt_dns_server_settings_list[0].id)

        # Update
        dns_server_group = self.ftd_client.get_dnsgroup_object_list(filter="name:My-Umbrella-Ella-Ella")
        mgmt_dns_server_settings.dnsServerGroup = dns_server_group[0]
        updated_mgmt_dns_server_settings = self.ftd_client.edit_mgmt_dns_settings(mgmt_dns_server_settings)
        self.assertEqual(updated_mgmt_dns_server_settings.dnsServerGroup.name, "My-Umbrella-Ella-Ella")

        # Delete - There is no delete APIs - DNS settings always exist

        # Revert DNS settings
        updated_mgmt_dns_server_settings.dnsServerGroup = mgmt_dns_server_settings_list[0].dnsServerGroup
        reverted_mgmt_dns_server_settings = self.ftd_client.edit_mgmt_dns_settings(updated_mgmt_dns_server_settings)
        self.assertEqual(reverted_mgmt_dns_server_settings.dnsServerGroup.name, "CiscoUmbrellaDNSServerGroup")

    def test_crud_operations_data_dns(self):
        # Create - There are no create APIs - DNS settings always exist

        # Read
        data_dns_server_settings_list = self.ftd_client.get_data_dns_settings_list()
        self.assertTrue(data_dns_server_settings_list)
        data_dns_server_settings = self.ftd_client.get_data_dns_settings(data_dns_server_settings_list[0].id)

        # Update
        dns_server_group = self.ftd_client.get_dnsgroup_object_list(filter="name:My-Umbrella-Ella-Ella")
        data_dns_server_settings.dnsServerGroup = dns_server_group[0]
        updated_data_dns_server_settings = self.ftd_client.edit_data_dns_settings(data_dns_server_settings)
        self.assertEqual(updated_data_dns_server_settings.dnsServerGroup.name, "My-Umbrella-Ella-Ella")

        # Revert DNS settings
        updated_data_dns_server_settings.dnsServerGroup = data_dns_server_settings_list[0].dnsServerGroup
        reverted_data_dns_server_settings = self.ftd_client.edit_data_dns_settings(updated_data_dns_server_settings)
        self.assertEqual(reverted_data_dns_server_settings.dnsServerGroup.name, "CiscoUmbrellaDNSServerGroup")
