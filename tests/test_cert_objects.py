from unittest import TestCase
from pyftd import FTDClient
from os import environ, getcwd


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

        src_test_files = {
            "ca_1_pem": "external_ca_1.pem",
            "ca_2_pem": "external_ca_2.pem",
            "int_ca_1_key": "internal_ca_1.key",
            "int_ca_2_key": "internal_ca_2.key",
            "int_ca_1_pem": "internal_ca_1.pem",
            "int_ca_2_pem": "internal_ca_2.pem",
            "server_key": "server.key",
            "server_1_cert": "server_1.pem",
            "server_2_cert": "server_2.pem",
        }

        self.test_certs = dict()
        for var_name, filename in src_test_files.items():
            with open(f"./tests/test_data/{filename}", "r") as file_obj:
                self.test_certs[var_name] = file_obj.read()

    def test_crud_operations_external_ca_certificates(self):
        # TEMP
        # cert = self.ftd_client.get_external_ca_certificate_list(filter="name:untitest-ca")
        # if cert:
        #     self.ftd_client.delete_external_ca_certificate(cert.id)

        # Create
        ext_ca_cert_obj = self.ftd_client.create_external_ca_certificate(
            {
                "name": "untitest-ca",
                "type": "externalcacertificate",
                "cert": self.test_certs["ca_1_pem"],
            }
        )
        self.assertEqual(ext_ca_cert_obj.name, "untitest-ca")
        # Read
        self.assertTrue(self.ftd_client.get_external_ca_certificate_list())
        self.assertEqual(self.ftd_client.get_external_ca_certificate(ext_ca_cert_obj.id), ext_ca_cert_obj)

        # update
        ext_ca_cert_obj.cert = self.test_certs["ca_2_pem"]
        updated_ext_ca_cert = self.ftd_client.edit_external_ca_certificate((ext_ca_cert_obj))

        # delete
        self.ftd_client.delete_external_ca_certificate(updated_ext_ca_cert.id)
        self.assertFalse(self.ftd_client.get_external_ca_certificate_list(filter="name:untitest-ca"))

    def test_crud_operations_internal_ca_certificates(self):
        # Create
        int_ca_cert_1 = self.ftd_client.create_internal_ca_certificate(
            {
                "name": "unittest-internal-ca",
                "certType": "UPLOAD",
                "type": "internalcacertificate",
                "cert": self.test_certs["int_ca_1_pem"],
                "privateKey": self.test_certs["int_ca_1_key"],
            }
        )
        self.assertEqual(int_ca_cert_1.name, "unittest-internal-ca")

        # Read
        self.assertEqual(self.ftd_client.get_internal_ca_certificate(int_ca_cert_1.id).id, int_ca_cert_1.id)

        # Update
        int_ca_cert_1.cert = self.test_certs["int_ca_2_pem"]
        int_ca_cert_1.privateKey = self.test_certs["int_ca_2_key"]
        updated_int_ca_cert_1 = self.ftd_client.edit_internal_ca_certificate(int_ca_cert_1)
        self.assertTrue(updated_int_ca_cert_1.cert, self.test_certs["int_ca_2_pem"])

        # Delete
        self.ftd_client.delete_internal_ca_certificate(int_ca_cert_1.id)
        self.assertFalse(self.ftd_client.get_internal_ca_certificate_list(filter="name:unittest-internal-ca"))

    def test_crud_operations_internal_certificates(self):
        # Create
        int_cert = self.ftd_client.create_internal_certificate(
            {
                "name": "unittest-internal-certificate",
                "certType": "UPLOAD",
                "type": "internalcertificate",
                "cert": self.test_certs["server_1_cert"],
                "privateKey": self.test_certs["server_key"],
            }
        )
        self.assertEqual(int_cert.name, "unittest-internal-certificate")

        # Read
        self.assertEqual(self.ftd_client.get_internal_certificate(int_cert.id).id, int_cert.id)

        # Update
        int_cert.cert = self.test_certs["server_2_cert"]
        int_cert.privateKey = self.test_certs["server_key"]
        updated_int_cert = self.ftd_client.edit_internal_certificate(int_cert)
        self.assertEqual(updated_int_cert.subjectCommonName, "hacksbrain2.com")

        # Delete
        self.ftd_client.delete_internal_certificate(updated_int_cert.id)
        self.assertFalse(self.ftd_client.get_internal_certificate_list(filter="name:unittest-internal-certificate"))

    def test_crud_operations_external_certificates(self):
        # Create
        ext_cert = self.ftd_client.create_external_certificate(
            {
                "name": "unittest-external-certificate",
                "certType": "UPLOAD",
                "type": "externalcertificate",
                "cert": self.test_certs["server_1_cert"],
                "privateKey": self.test_certs["server_key"],
            }
        )

        self.assertEqual(ext_cert.name, "unittest-external-certificate")

        # Read
        self.assertEqual(self.ftd_client.get_external_certificate(ext_cert.id).id, ext_cert.id)

        # Update
        ext_cert.cert = self.test_certs["server_2_cert"]
        ext_cert.privateKey = self.test_certs["server_key"]
        updated_ext_cert = self.ftd_client.edit_external_certificate(ext_cert)
        self.assertEqual(updated_ext_cert.name, "unittest-external-certificate")

        # Delete
        self.ftd_client.delete_external_certificate(updated_ext_cert.id)
        self.assertFalse(self.ftd_client.get_external_certificate_list(filter="name:unittest-external-certificate"))
