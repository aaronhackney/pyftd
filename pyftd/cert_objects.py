import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDCertificateObjects:
    ################################
    # External CA Certificates
    @FTDAPIWrapper()
    def get_external_ca_certificate_list(
        self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        """
        Get a list of External CA certificates - Returns a list of the common public CAs as well as any CAs uploaded
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        return: list of ExternalCACertificate objects
        :rtype: list
        """
        return (
            self.swagger_client.Certificate.getExternalCACertificateList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_external_ca_certificate(self, obj_id: str) -> dict:
        """
        Get a specific external ca certificate
        :param obj_id: uuid of the certificate object to retrieve
        :return: ExternalCACertificate
        :rtype: ExternalCACertificateWrapper
        """
        return self.swagger_client.Certificate.getExternalCACertificate(objId=obj_id).result()

    @FTDAPIWrapper()
    def create_external_ca_certificate(self, certificate_obj: dict) -> dict:
        """
        Upload/Add an external CA certificate we wish to trust in the ExternalCACertificate data format.
        ExternalCACertificate Format:
        {
            "name": "untitest-ca",
            "type": "externalcacertificate",
            "cert": "-----BEGIN CERTIFICATE-----\n...xxxxxxxxxxxxxxx...\n-----END CERTIFICATE-----",
        }
        :param certificate_obj:
        :return: ExternalCACertificate
        :rtype: ExternalCACertificate
        """
        return self.swagger_client.Certificate.addExternalCACertificate(body=certificate_obj).result()

    @FTDAPIWrapper()
    def edit_external_ca_certificate(self, certificate_obj: dict) -> dict:
        """
        :param certificate_obj: The certificate object we wish to update. See the API explorer for more fields
        :return: ExternalCACertificate
        :rtype: ExternalCACertificate
        """
        return self.swagger_client.Certificate.editExternalCACertificate(
            objId=certificate_obj.id, body=certificate_obj
        ).result()

    @FTDAPIWrapper()
    def delete_external_ca_certificate(self, obj_id: str) -> None:
        """
        :param obj_id: ExternalCACertificate object id that we wish to delete
        :return: None
        """
        return self.swagger_client.Certificate.deleteExternalCACertificate(objId=obj_id).result()

    ################################
    # Internal CA Certificates
    @FTDAPIWrapper()
    def get_internal_ca_certificate_list(self, filter=""):
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        """
        :param search: optional search. Exmaple: "filter=name~my-certificate"
        :return: list of InternalCACertificates
        """
        return self.swagger_client.Certificate.getInternalCACertificateList(filter=filter, limit=9999).result().items

    @FTDAPIWrapper()
    def get_internal_ca_certificate(self, obj_id: str) -> list:
        """
        :param obj_id: InternalCACertificate object id we wish to retrieve
        :return: InternalCACertificate
        """
        return self.swagger_client.Certificate.getInternalCACertificate(objId=obj_id).result()

    @FTDAPIWrapper()
    def create_internal_ca_certificate(self, certificate_obj):
        """
        Upload/Add an internal CA certificate in the InternalCACertificate data format.
        Note that the privateKey must be unencrypted.
        InternalCACertificate Format:
        {
            "name": "unittest-internal-ca",
            "certType": "UPLOAD", ['UPLOAD', 'SELFSIGNED']
            "type": "internalcacertificate",
            "cert": xxxxxx,
            "privateKey": xxxxxxxx
        }
        :param certificate_obj:
        :return: InternalCACertificate
        :rtype: InternalCACertificate
        """
        return self.swagger_client.Certificate.addInternalCACertificate(body=certificate_obj).result()

    @FTDAPIWrapper()
    def edit_internal_ca_certificate(self, certificate_obj):
        """
        :param certificate_obj: The certificate object we wish to update. See the API explorer for more fields
        :return: InternalCACertificate
        :rtype: InternalCACertificate
        """
        return self.swagger_client.Certificate.editInternalCACertificate(
            objId=certificate_obj.id, body=certificate_obj
        ).result()

    @FTDAPIWrapper()
    def delete_internal_ca_certificate(self, obj_id):
        """
        :param obj_id: InternalCACertificate object id that we wish to delete
        :return: None
        """
        return self.swagger_client.Certificate.deleteInternalCACertificate(objId=obj_id).result()

    ################################
    # Internal Certificates
    @FTDAPIWrapper()
    def get_internal_certificate_list(self, filter=""):
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        """
        :param search: optional search. Exmaple: "filter=name~my-certificate"
        :return: list of InternalCertificate
        """
        return self.swagger_client.Certificate.getInternalCertificateList(filter=filter, limit=9999).result().items

    @FTDAPIWrapper()
    def get_internal_certificate(self, obj_id):
        """
        :param obj_id: InternalCertificate object id we wish to retrieve
        :return: InternalCertificate
        """
        return self.swagger_client.Certificate.getInternalCertificate(objId=obj_id).result()

    @FTDAPIWrapper()
    def create_internal_certificate(self, certificate_obj):
        """
        Upload/Add an internal CA certificate in the InternalCACertificate data format.
        Note that the privateKey must be unencrypted.
        InternalCACertificate Format:
        {
            "name": "unittest-internal-certificate",
            "certType": "UPLOAD",
            "type": "internalcertificate",
            "cert": xxxxxx,
            "privateKey": xxxxxxxx
        }
        :param certificate_obj:
        :return: InternalCertificate
        :rtype: InternalCertificate
        """
        return self.swagger_client.Certificate.addInternalCertificate(body=certificate_obj).result()

    @FTDAPIWrapper()
    def edit_internal_certificate(self, certificate_obj):
        """
        :param certificate_obj: The certificate object we wish to update. See the API explorer for more fields
        :return: InternalCertificate
        :rtype: InternalCertificate
        """
        return self.swagger_client.Certificate.editInternalCertificate(
            objId=certificate_obj.id, body=certificate_obj
        ).result()

    @FTDAPIWrapper()
    def delete_internal_certificate(self, obj_id):
        """
        :param obj_id: InternalCACertificate object id that we wish to delete
        :return: None
        """
        return self.swagger_client.Certificate.deleteInternalCertificate(objId=obj_id).result()

    @FTDAPIWrapper()
    def get_external_certificate_list(self, filter=""):
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        """
        :param search: optional search. Exmaple: "filter=name~my-certificate"
        :return: list of ExternalCertificate
        """
        return self.swagger_client.Certificate.getExternalCertificateList(filter=filter, limit=9999).result().items

    @FTDAPIWrapper()
    def get_external_certificate(self, obj_id):
        """
        :param obj_id: ExternalCertificate object id we wish to retrieve
        :return: ExternalCertificate
        """
        return self.swagger_client.Certificate.getExternalCertificate(objId=obj_id).result()

    @FTDAPIWrapper()
    def create_external_certificate(self, certificate_obj):
        """
        Upload/Add an external CA certificate in the ExternalCACertificate data format.
        Note that the privateKey must be unencrypted.
        ExternalCACertificate Format:
        {
            "name": "unittest-external-certificate",
            "certType": "UPLOAD",
            "type": "externalcertificate",
            "cert": xxxxxx,
            "privateKey": xxxxxxxx
        }
        :param certificate_obj:
        :return: ExternalCertificate
        :rtype: ExternalCertificate
        """
        return self.swagger_client.Certificate.addExternalCertificate(body=certificate_obj).result()

    @FTDAPIWrapper()
    def edit_external_certificate(self, certificate_obj):
        """
        :param certificate_obj: The certificate object we wish to update. See the API explorer for more fields
        :return: ExternalCertificate
        :rtype: ExternalCertificate
        """
        return self.swagger_client.Certificate.editExternalCertificate(
            objId=certificate_obj.id, body=certificate_obj
        ).result()

    @FTDAPIWrapper()
    def delete_external_certificate(self, obj_id):
        """
        :param obj_id: ExternalCACertificate object id that we wish to delete
        :return: None
        """
        return self.swagger_client.Certificate.deleteExternalCertificate(objId=obj_id).result()
