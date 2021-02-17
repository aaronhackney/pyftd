from unittest import TestCase
from pyftd import FTDClient
from os import environ


class TestSyslogDNSObjects(TestCase):
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
    # DNSGroup Objects
    def test_crud_operations_dnsgroup_objects(self):
        # Create
        dns_grp_obj = self.ftd_client.create_dnsgroup_object(
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
        self.assertEqual(dns_grp_obj.name, "My-Umbrella-Ella-Ella")

        # Read
        self.assertEqual(self.ftd_client.get_dnsgroup_object(dns_grp_obj.id).id, dns_grp_obj.id)

        # Update
        dns_grp_obj.dnsServers = [{"ipAddress": "208.67.222.222", "type": "dnsserver"}]
        updated_dns_grp_obj = self.ftd_client.edit_dnsgroup_object(dns_grp_obj)
        self.assertEqual(len(self.ftd_client.get_dnsgroup_object(updated_dns_grp_obj.id).dnsServers), 1)

        # Delete
        self.ftd_client.delete_dnsgroup_object(updated_dns_grp_obj.id)
        self.assertFalse(self.ftd_client.get_dnsgroup_object_list(filter="name:My-Umbrella-Ella-Ella"))

    #############################
    # Syslog Objects
    def test_crud_operations_syslog_servers(self):
        # Create
        syslog_obj = self.ftd_client.create_syslog_server_object(
            {
                "name": "ElkStack",
                "useManagementInterface": True,
                "protocol": "UDP",
                "host": "172.30.4.100",
                "port": "514",
                "type": "syslogserver",
            }
        )

        # Read
        self.assertEqual(self.ftd_client.get_syslog_server_object(syslog_obj.id).id, syslog_obj.id)

        # Update
        syslog_obj.protocol = "TCP"
        syslog_obj.port = "1470"
        updated_syslog_obj = self.ftd_client.edit_syslog_server_object(syslog_obj)
        self.assertEqual(updated_syslog_obj.protocol, "TCP")

        # Delete
        self.ftd_client.delete_syslog_server_object(updated_syslog_obj.id)
        self.assertFalse(self.ftd_client.get_syslog_server_object_list(filter="name:ElkStack"))
