import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDURLObjects:
    @FTDAPIWrapper()
    def get_url_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of URLObject objects
        :rtype: list
        """
        return self.swagger_client.URLObject.getURLObjectList(limit=limit, offset=offset, filter=filter).result().items

    @FTDAPIWrapper()
    def get_url_object(self, url_id: str) -> dict:
        """
        Get a specific url object
        :param url_id: uuid of a url object
        :return: URLObject object
        :rtype: URLObjectWrapper
        """
        return self.swagger_client.URLObject.getURLObject(objId=url_id).result()

    @FTDAPIWrapper()
    def create_url_object(self, url_obj: dict) -> dict:
        """
        Add a url object
        :param url_obj: dict dictionary of the URL object to add
            {
                "name": "test-url"
                "url": "www.example.com",
                "description": "test url object",
                "type": "urlobject",
            }
        :return: URLObject object
        :rtype: URLObjectWrapper
        """
        return self.swagger_client.URLObject.addURLObject(body=url_obj).result()

    @FTDAPIWrapper()
    def edit_url_object(self, url_obj: dict) -> dict:
        """
        Edit an existing url object
        :param url_obj: dict (URLObject)
        :return: URLObject
        :rtype: URLObjectWrapper
        """
        return self.swagger_client.URLObject.editURLObject(body=url_obj, objId=url_obj.id).result()

    @FTDAPIWrapper()
    def delete_url_object(self, url_id: str) -> None:
        """
        Delete an existing URL object
        :param url_id: uuid of the url object
        :return: none
        """
        return self.swagger_client.URLObject.deleteURLObject(objId=url_id).result()

    @FTDAPIWrapper()
    def get_url_object_group_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get a list of URLObjectGroup objects
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of URLObjectGroup objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.URLObject.getURLObjectGroupList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_url_object_group(self, url_group_id: str) -> dict:
        """
        Get an existing urlobject group
        :param url_group_id: uuid of the url object group
        :return: URLObjectGroup
        :rtype: URLObjectGroupWrapper
        """
        return self.swagger_client.URLObject.getURLObjectGroup(objId=url_group_id).result()

    @FTDAPIWrapper()
    def create_url_object_group(self, url_obj_grp: dict) -> dict:
        """
        Create a URLObjectGroup object
        url_obj_grp = {
                        "description":"test 123",
                        "name":"test",
                        "objects":[ {url_obj_1}, {url_obj_2} ],
                        "type":"urlobjectgroup",
                      }
        :return: URLObjectGroup
        :rtype: URLObjectGroupWrapper
        """
        return self.swagger_client.URLObject.addURLObjectGroup(body=url_obj_grp).result()

    @FTDAPIWrapper()
    def edit_url_object_group(self, url_group_obj: str) -> dict:
        """
        Edit an existing url group object
        :param url_group_obj: URLObjectGroup object
        :return: URLObjectGroup
        :rtype: URLObjectGroupWrapper
        """
        return self.swagger_client.URLObject.editURLObjectGroup(body=url_group_obj, objId=url_group_obj.id).result()

    @FTDAPIWrapper()
    def delete_url_object_group(self, url_group_id: str) -> None:
        """
        Delete a URLObjectGroup object
        :param url_group_id: uuid of the URLObjectGroup object
        :return: none
        """
        return self.swagger_client.URLObject.deleteURLObjectGroup(objId=url_group_id).result()