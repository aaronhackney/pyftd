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

        # Load test external CA certificates
        with open("./tests/test_data/external_ca_1.pem", "r") as file_object:
            self.ca_1_pem = file_object.read()
        with open("./tests/test_data/external_ca_2.pem", "r") as file_object:
            self.ca_2_pem = file_object.read()

        # Load test internal CA key and certs
        with open("./tests/test_data/internal_ca_1.key", "r") as file_object:
            self.int_ca_1_key = file_object.read()
        with open("./tests/test_data/internal_ca_1.pem", "r") as file_object:
            self.int_ca_1_pem = file_object.read()
        with open("./tests/test_data/internal_ca_2.key", "r") as file_object:
            self.int_ca_2_key = file_object.read()
        with open("./tests/test_data/internal_ca_2.pem", "r") as file_object:
            self.int_ca_2_pem = file_object.read()

    def test_crud_operations_external_ca_certificates(self):

        # Create
        ext_ca_cert_obj = self.ftd_client.create_external_ca_certificate(
            {
                "name": "untitest-ca",
                "type": "externalcacertificate",
                "cert": self.ca_1_pem,
            }
        )
        self.assertEqual(ext_ca_cert_obj.name, "untitest-ca")
        # Read
        self.assertTrue(self.ftd_client.get_external_ca_certificate_list())
        self.assertEqual(self.ftd_client.get_external_ca_certificate(ext_ca_cert_obj.id), ext_ca_cert_obj)

        # update
        ext_ca_cert_obj.cert = self.ca_2_pem
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
                "cert": self.int_ca_1_pem,
                "privateKey": self.int_ca_1_key,
            }
        )
        self.assertEqual(int_ca_cert_1.name, "unittest-internal-ca")

        # Read
        self.assertEqual(self.ftd_client.get_internal_ca_certificate(int_ca_cert_1.id).id, int_ca_cert_1.id)

        # Update
        int_ca_cert_1.cert = self.int_ca_2_pem
        int_ca_cert_1.privateKey = self.int_ca_2_key
        updated_int_ca_cert_1 = self.ftd_client.edit_internal_ca_certificate(int_ca_cert_1)
        self.assertTrue(updated_int_ca_cert_1.cert, self.int_ca_2_pem)

        # Delete
        self.ftd_client.delete_internal_ca_certificate(int_ca_cert_1.id)
        self.assertFalse(self.ftd_client.get_internal_ca_certificate_list(filter="name:unittest-internal-ca"))

    def test_crud_operations_internal_certificates(self):
        # Create
        int_cert = self.ftd_client.create_internal_certificate()