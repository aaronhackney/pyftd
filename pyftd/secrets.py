import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDSecretObjects:
    @FTDAPIWrapper()
    def get_secret_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of Secret objects
        :rtype: list
        """
        return self.swagger_client.Secret.getSecretList(limit=limit, offset=offset, filter=filter).result().items

    @FTDAPIWrapper()
    def get_secret_object(self, secret_obj_id: str) -> dict:
        """
        Get a specific secret object
        :param secret_obj_id: uuid of secret object
        :return: SecretWrapper
        """
        return self.swagger_client.Secret.getSecret(objId=secret_obj_id).result()

    @FTDAPIWrapper()
    def create_secret_object(self, secret_obj: dict) -> dict:
        """
        Create a secret object
        :param secret_obj: dict = {
                                    "name": secret_name,
                                    "password": password,
                                    "description": description,
                                    "type": "secret",
                                  }
        :return: dict Secret object
        :rtype: dict SecretWrapper
        """
        return self.swagger_client.Secret.addSecret(body=secret_obj).result()

    @FTDAPIWrapper()
    def edit_secret_object(self, secret_obj) -> dict:
        """
        Edit a secret object
        :param secret_obj: dict
        :return: dict Secret object
        :rtype: dict SecretWrapper
        """
        return self.swagger_client.Secret.editSecret(body=secret_obj, objId=secret_obj.id).result()

    @FTDAPIWrapper()
    def delete_secret_object(self, secret_obj_id: str) -> None:
        """
        Delete a secret object
        :param secret_obj_id: str uuid of the secret object
        """
        return self.swagger_client.Secret.deleteSecret(objId=secret_obj_id).result()
