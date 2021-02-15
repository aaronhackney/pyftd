from unittest import TestCase
from pyftd import FTDClient
from random import randint
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
        self.ftd_client.get_access_token()
        self.ftd_client.get_swagger_client()

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


#    def test_edit_url_object_group(self):
#        url_objects = self.generate_random_url_objects()
#        url_group = self.create_url_object_group_data("test-url-group", url_objects)
#        self.assertIsNotNone(url_group)
#        url_group_count = len(url_group.objects)
#        url_objects.append(self.ftd_client.add_url_object(f"new-{str(randint(0,1000))}", f"{str(randint(0,1000))}.com"))
#        url_group.objects = url_objects
#        url_group = self.ftd_client.edit_url_object_group(url_group)
#        self.assertEquals(url_group_count + 1, len(url_group.objects))
#        self.ftd_client.delete_url_object_group(url_group.id)
#        self.delete_url_objects(url_objects)
#
#    def test_get_url_object_group_list(self):
#        url_objects = self.generate_random_url_objects()
#        url_object_group = self.create_url_object_group_data("test-url-group", url_objects)
#        self.assertTrue(self.ftd_client.get_url_object_group_list())
#        self.ftd_client.delete_url_object_group(url_object_group.id)
#        self.delete_url_objects(url_objects)
#
#    def test_search_url_object_group_list(self):
#        url_objects = self.generate_random_url_objects()
#        url_object_group = self.create_url_object_group_data("test-url-group", url_objects)
#        self.assertTrue(self.ftd_client.get_url_object_group_list(search="name:test-url-group"))
#        self.ftd_client.delete_url_object_group(url_object_group.id)
#        self.delete_url_objects(url_objects)
#
#    def create_url_object_group_data(self, group_name, url_objects):
#        self.remove_existing_group(group_name)
#        return self.ftd_client.add_url_object_group(group_name, url_objects)
#
#    def remove_existing_group(self, group_name):
#        existing_group = self.ftd_client.get_url_object_group_list(search=f"name:{group_name}")
#        if existing_group:
#            self.ftd_client.delete_url_object_group(existing_group[0].id)
#
#    def generate_random_url_objects(self, num_objs=3):
#        url_objects = []
#        for x in range(0, num_objs):
#            url_objects.append(
#                self.ftd_client.add_url_object(f"test-{str(randint(0,1000))}", f"{str(randint(0,1000))}.com")
#            )
#        return url_objects
#
#    def delete_url_objects(self, url_object_list):
#        for url_object in url_object_list:
#            self.ftd_client.delete_url_object(url_object.id)
#
#    def test_add_fqdn_network_object(self):
#        test_url = f"{str(randint(0,1000))}.com"
#        fqdn_net_obj = self.ftd_client.add_network_object(test_url, "FQDN", test_url, dns_resolution="IPV4_AND_IPV6")
#        self.assertIsNotNone(fqdn_net_obj)
#        self.ftd_client.delete_network_object(fqdn_net_obj.id)
#
#    def test_delete_fqdn_network_object(self):
#        test_url = f"{str(randint(0,1000))}.com"
#        fqdn_net_obj = self.ftd_client.add_network_object(test_url, "FQDN", test_url, dns_resolution="IPV4_AND_IPV6")
#        self.assertTrue(self.ftd_client.get_network_object_list(search=f"name:{test_url}"))
#        self.ftd_client.delete_network_object(fqdn_net_obj.id)
#        self.assertFalse(self.ftd_client.get_network_object_list(search=f"name:{test_url}"))
#
#    def test_edit_fqdn_network_object(self):
#        test_url = f"{str(randint(0,1000))}.com"
#        fqdn_net_obj = self.ftd_client.add_network_object(test_url, "FQDN", test_url, dns_resolution="IPV4_AND_IPV6")
#        fqdn_net_obj.value = "hacksbrain.com"
#        fqdn_net_obj = self.ftd_client.edit_network_object(fqdn_net_obj)
#        self.assertEquals(fqdn_net_obj.value, "hacksbrain.com")
#        self.ftd_client.delete_network_object(fqdn_net_obj.id)
#

#    def test_delete_tcp_object(self):
#        my_tcp_port = self.ftd_client.add_tcp_port_object("unit-test-port-666", "666", description="unit test tcp port")
#        self.assertIsNotNone(my_tcp_port)
#        self.ftd_client.delete_tcp_port_object(my_tcp_port.id)
#
#    def test_delete_udp_object(self):
#        my_udp_port = self.ftd_client.add_udp_port_object("unit-test-port-666", "666", description="unit test udp port")
#        self.assertIsNotNone(my_udp_port)
#        self.ftd_client.delete_udp_port_object(my_udp_port.id)
#        search_result = self.ftd_client.get_udp_port_object_list(search=f"name:unit-test-port-666")
#        self.assertFalse(search_result)
#
#    def test_delete_icmp_object(self):
#        my_icmp_port = self.ftd_client.add_icmpv4_port_object("my_test_icmp_obj", icmpv4type="ECHO_REQUEST")
#        self.assertIsNotNone(my_icmp_port)
#        self.ftd_client.delete_icmp_port_object(my_icmp_port.id)
#        search_result = self.ftd_client.get_port_object_by_name("my_test_icmp_obj")
#        self.assertFalse(search_result)
#
#    def test_get_port_object_by_name_tcp(self):
#        my_tcp_port = self.ftd_client.add_tcp_port_object("unit-test-port-666", "666", description="unit test tcp port")
#        self.assertIsNotNone(my_tcp_port)
#        search_result = self.ftd_client.get_port_object_by_name("unit-test-port-666")
#        self.assertIsNotNone(search_result)
#        self.ftd_client.delete_tcp_port_object(my_tcp_port.id)
#        my_udp_port = self.ftd_client.add_udp_port_object("unit-test-port-666", "666", description="unit test udp port")
#        self.assertIsNotNone(my_udp_port)
#        search_result = self.ftd_client.get_port_object_by_name("unit-test-port-666")
#        self.assertIsNotNone(search_result)
#        self.ftd_client.delete_udp_port_object(my_udp_port.id)
#
#    def test_get_port_object_by_name_icmp(self):
#        my_icmp_port = self.ftd_client.add_icmpv4_port_object("my_test_icmp_obj", icmpv4type="ECHO_REQUEST")
#        self.assertIsNotNone(my_icmp_port)
#        search_result = self.ftd_client.get_port_object_by_name("my_test_icmp_obj")
#        self.assertIsNotNone(search_result)
#        self.ftd_client.delete_icmp_port_object(my_icmp_port.id)
#
#    def test_get_external_ca_certificate_list(self):
#        certificate_list = self.ftd_client.get_external_ca_certificate_list()
#        self.assertTrue(certificate_list)
#
#    def test_get_external_ca_certificate(self):
#        certificate_list = self.ftd_client.get_external_ca_certificate_list()
#        certificate = self.ftd_client.get_external_ca_certificate(certificate_list[0].id)
#        self.assertIsNotNone(certificate)
#
#    def test_add_edit_delete_external_ca_certificate(self):
#
#        cert_obj = {
#            "name": "untitest-ca",
#            "type": "externalcacertificate",
#            "cert": self.ca_certificate,
#        }
#
#        certificate_list = self.ftd_client.get_external_ca_certificate_list(search="name~untitest-ca")
#        if certificate_list:
#            self.ftd_client.delete_external_ca_certificate(certificate_list[0].id)
#
#        # Create test
#        new_ca_cert = self.ftd_client.add_external_ca_certificate(cert_obj)
#        self.assertIsNotNone(new_ca_cert)
#
#        # edit test
#        original_subject_dn = new_ca_cert.subjectDistinguishedName
#        new_ca_cert.cert = self.ca_certificate_2
#        new_ca_cert = self.ftd_client.edit_external_ca_certificate(new_ca_cert)
#        self.assertNotEquals(original_subject_dn, new_ca_cert.subjectDistinguishedName)
#
#        # Delete test
#        deleted_operation = self.ftd_client.delete_external_ca_certificate(new_ca_cert.id)
#        self.assertIsNone(deleted_operation)
#
#    def test_get_internal_ca_certificate_list(self):
#        internal_ca_list = self.ftd_client.get_internal_ca_certificate_list()
#        self.assertIsNotNone(internal_ca_list)
#
#    def test_get_internal_ca_certificate(self):
#        internal_ca_list = self.ftd_client.get_internal_ca_certificate_list()
#        internal_ca = self.ftd_client.get_internal_ca_certificate(internal_ca_list[0].id)
#        self.assertIsNotNone(internal_ca)
#
#    def test_add_internal_ca_certificate(self):
#        internal_ca_list = self.ftd_client.get_internal_ca_certificate_list()
#        for internal_ca in internal_ca_list:
#            if internal_ca.name == "unittest-internal-ca":
#                self.ftd_client.delete_internal_ca_certificate(internal_ca.id)
#        internal_ca_cert = {
#            "name": "unittest-internal-ca",
#            "certType": "UPLOAD",
#            "type": "internalcacertificate",
#            "cert": self.internal_ca_1,
#            "privateKey": self.internal_ca_key,
#        }
#
#        new_internal_ca_cert_obj = self.ftd_client.add_internal_ca_certificate(internal_ca_cert)
#        self.assertIsNotNone(new_internal_ca_cert_obj)
#
#        original_ca_cert_cn = new_internal_ca_cert_obj.issuerCommonName
#        new_internal_ca_cert_obj.cert = self.internal_ca_2
#        new_internal_ca_cert_obj.privateKey = self.internal_ca_key
#        new_internal_ca_cert_obj = self.ftd_client.edit_internal_ca_certificate(new_internal_ca_cert_obj)
#        self.assertNotEquals(original_ca_cert_cn, new_internal_ca_cert_obj.issuerCommonName)
#
#        delete_operation = self.ftd_client.delete_internal_ca_certificate(new_internal_ca_cert_obj.id)
#        self.assertIsNone(delete_operation)
#
#    def test_get_internal_certificate_list(self):
#        internal_cert_list = self.ftd_client.get_internal_certificate_list()
#        self.assertTrue(internal_cert_list)
#
#    def test_get_internal_certificate(self):
#        internal_cert_list = self.ftd_client.get_internal_certificate_list()
#        internal_cert = self.ftd_client.get_internal_certificate(internal_cert_list[0].id)
#        self.assertIsNotNone(internal_cert)
#
#    def test_add_edit_delete_internal_certificate(self):
#        internal_cert_list = self.ftd_client.get_internal_certificate_list()
#        for internal_cert in internal_cert_list:
#            if internal_cert.name == "unittest-internal-certificate":
#                self.ftd_client.delete_internal_certificate(internal_cert.id)
#
#        # Test add certificate
#        internal_cert = {
#            "name": "unittest-internal-certificate",
#            "certType": "UPLOAD",
#            "type": "internalcertificate",
#            "cert": self.internal_certificate_1,
#            "privateKey": self.internal_certificate_1_key,
#        }
#        internal_cert_obj = self.ftd_client.add_internal_certificate(internal_cert)
#        self.assertIsNotNone(internal_cert_obj)
#
#        # Test edit certificate
#        original_cert_cn = internal_cert_obj.subjectCommonName
#        internal_cert_obj.cert = self.internal_certificate_2
#        internal_cert_obj.privateKey = self.internal_certificate_2_key
#        internal_cert_obj = self.ftd_client.edit_internal_certificate(internal_cert_obj)
#        self.assertNotEquals(original_cert_cn, internal_cert_obj.subjectCommonName)
#
#        # Test delete certificate
#        delete_operation = self.ftd_client.delete_internal_certificate(internal_cert_obj.id)
#        self.assertIsNone(delete_operation)
#
#    def test_get_external_certificate_list(self):
#        external_cert_list = self.ftd_client.get_external_certificate_list()
#        self.assertTrue(external_cert_list)
#
#    def test_get_external_certificate(self):
#        external_cert_list = self.ftd_client.get_external_certificate_list()
#        external_cert = self.ftd_client.get_external_certificate(external_cert_list[0].id)
#        self.assertIsNotNone(external_cert)
#
#    def test_add_edit_delete_external_certificate(self):
#        external_cert_list = self.ftd_client.get_external_certificate_list()
#        for external_cert in external_cert_list:
#            if external_cert.name == "unittest-external-certificate":
#                self.ftd_client.delete_external_certificate(external_cert.id)
#
#        # Test add certificate
#        external_cert = {
#            "name": "unittest-external-certificate",
#            "certType": "UPLOAD",
#            "type": "externalcertificate",
#            "cert": self.internal_certificate_1,
#        }
#        external_cert_obj = self.ftd_client.add_external_certificate(external_cert)
#        self.assertIsNotNone(external_cert_obj)
#
#        # Test edit certificate
#        original_cert_cn = external_cert_obj.subjectCommonName
#        external_cert_obj.cert = self.internal_certificate_2
#        external_cert_obj.privateKey = self.internal_certificate_2_key
#        external_cert_obj = self.ftd_client.edit_external_certificate(external_cert_obj)
#        self.assertNotEquals(original_cert_cn, external_cert_obj.subjectCommonName)
#
#        # Test delete certificate
#        delete_operation = self.ftd_client.delete_external_certificate(external_cert_obj.id)
#        self.assertIsNone(delete_operation)
