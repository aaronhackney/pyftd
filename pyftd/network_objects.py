import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDNetworkObjects:
    @FTDAPIWrapper()
    def get_network_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: network object(s) we wish to search for like "name:obj-1.1.1.1" or "fts~1.1.1.1"
        :return: list of network objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.NetworkObject.getNetworkObjectList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_network_object(self, obj_id: str) -> dict:
        """
        return a network object given an object id
        :param obj_id: uuid of the network object
        :return: NetworkObject
        :rtype: NetworkObjectWrapper
        """
        return self.swagger_client.NetworkObject.getNetworkObject(objId=obj_id).result()

    @FTDAPIWrapper()
    def create_network_object(self, network_obj: dict) -> dict:
        """
        Add a network object of subType host, network, range, or fqdn
        :param: network_obj: dict {
                                    "name": "my_obj",
                                    "description": "My cool object",
                                    "subType": ['HOST', 'NETWORK', 'RANGE', 'FQDN'],
                                    "value": '10.10.10.1',
                                    "dnsResolution": ['IPV4_ONLY', 'IPV6_ONLY', 'IPV4_AND_IPV6'],
                                    "type": "networkobject",
                                  }
        :return: created network object
        :rtype: NetworkObjectWrapper
        """
        return self.swagger_client.NetworkObject.addNetworkObject(body=network_obj).result()

    @FTDAPIWrapper()
    def edit_network_object(self, network_obj):
        """
        Edit an existing network object
        :param network_object: NetworkObject
        :type network_object: NetworkObjectWrapper
        :return: NetworkObjectWrapper
        :rtype: NetworkObjectWrapper
        """
        return self.swagger_client.NetworkObject.editNetworkObject(body=network_obj, objId=network_obj.id).result()

    @FTDAPIWrapper()
    def delete_network_object(self, network_obj_id: str) -> None:
        """
        Delete an existing network object
        :param network_object_id: uuid of the object
        :return: none
        """
        return self.swagger_client.NetworkObject.deleteNetworkObject(objId=network_obj_id).result()

    @FTDAPIWrapper()
    def get_network_object_group_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        return a list of network object groups
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: network object we wish to search for like "name:obj-1.1.1.1" or "fts~1.1.1.1"
        :return: list of NetworkObjectGroup objects
        :rtype: NetworkObjectGroupWrapper
        """
        return (
            self.swagger_client.NetworkObject.getNetworkObjectGroupList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_network_object_group(self, obj_id: str) -> dict:
        """
        Get an existing network object group
        :param obj_id: uuid of network object group
        :return: NetworkObjectGroup object
        :rtype: NetworkObjectGroupWrapper
        """
        return self.swagger_client.NetworkObject.getNetworkObjectGroup(objId=obj_id).result()

    @FTDAPIWrapper()
    def create_network_object_group(self, net_obj_grp: dict) -> dict:
        """
        Add a network object group
        :param net_obj_grp: dict {
                                    "name": my-obj-group",
                                    "description": "My cool group",
                                    "objects": [list of network objects],
                                    "type": "networkobjectgroup",
                                 }
        :return: NetworkObjectGroup object
        :rtype: NetworkObjectGroupWrapper
        """
        return self.swagger_client.NetworkObject.addNetworkObjectGroup(body=net_obj_grp).result()

    @FTDAPIWrapper()
    def delete_network_object_group(self, obj_group_id: str) -> None:
        """
        Delete an object-group
        :param obj_group_id: uuid of the object group
        :return: none
        """
        return self.swagger_client.NetworkObject.deleteNetworkObjectGroup(objId=obj_group_id).result()

    @FTDAPIWrapper()
    def edit_network_object_group(self, obj_group: dict) -> dict:
        """
        Edit an existing object-group
        :param obj_group: NetworkObjectGroup object
        :return: NetworkObjectGroup
        :rtype: NetworkObjectGroupWrapper
        """
        return self.swagger_client.NetworkObject.editNetworkObjectGroup(body=obj_group, objId=obj_group.id).result()
