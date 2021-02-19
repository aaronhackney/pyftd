import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDInterfaces:
    ################################
    # Physical Interface Objects
    @FTDAPIWrapper()
    def get_physical_interface_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get a list of physical interfaces
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of interface objects
        :rtype: list
        """
        return (
            self.swagger_client.Interface.getPhysicalInterfaceList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    def get_physical_interface(self, physical_int_obj_id):
        """
        Given a physical interface object ID, return the physical interface object
        """
        return self.swagger_client.Interface.getPhysicalInterface(objId=physical_int_obj_id).result()

    def edit_physical_interface(self, physical_int_obj):
        """
        Edit the settings of an interface
        Note: Not all parameters are required. If you only want IPv4, for example, you can omit the IPv6 config
        See the ApiBrowser for full details on all of the options an possible values, incuding ipv6
        :param physical_int_obj: dict {
                                        "name":"dmz",
                                        "duplexType":"AUTO",
                                        "speedType":"AUTO",
                                        "mode":"ROUTED",
                                        "type":"physicalinterface",
                                        "security":0,
                                        "enabled":true,
                                        "hardwareName":"GigabitEthernet0/2",
                                        "description":"dmz inteface",
                                        "ipv4": {
                                          "ipType": "STATIC",
                                          "type": "interfaceipv4",
                                          "ipAddress": {
                                            "standbyIpAddress": "192.168.200.2",
                                            "type": "haipv4address",
                                            "netmask": "255.255.255.0",
                                            "ipAddress": "192.168.200.1"
                                          }
                                        }
                                      }
        return: dict
        rtype: dict
        """
        return self.swagger_client.Interface.editPhysicalInterface(
            body=physical_int_obj, objId=physical_int_obj.id
        ).result()

    ################################
    # Sub-Interface Objects
    @FTDAPIWrapper()
    def get_sub_interface_list(
        self, parent_interface_id: str, limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        """Given a parentId (physical interface object id), get all sub-interface configurations
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of all sub-interface details for a given physical interface
        :rtype: list
        """
        return (
            self.swagger_client.Interface.getSubInterfaceList(
                parentId=parent_interface_id, limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_sub_interface(self, parent_interface_id: str, sub_interface_id: str) -> dict:
        """Given a parentId (physical interface object id) and a sunb interface id, get this sub-interface configuration
        :return: dict of sub-interface details
        :rtype: dict
        """
        return self.swagger_client.Interface.getSubInterface(
            parentId=parent_interface_id, objId=sub_interface_id
        ).result()

    @FTDAPIWrapper()
    def create_sub_interface(self, parent_interface_id: str, sub_int_obj: dict) -> dict:
        """
        Given a sub-interface configuration (dict), create the sub interface
        :param parent_interface_id: str the physical interface on which to create the sub interface
        :param sub_int_obj: dict {
                                      "type": "subinterface",
                                      "subIntfId": 101,
                                      "vlanId": 101,
                                      "mode": "ROUTED",
                                      "present": true,
                                      "security": 0,
                                      "enabled": true,
                                      "hardwareName": "GigabitEthernet0/0.101",
                                      "description": "VLAN 101 Sub Interface",
                                      "monitorInterface": true,
                                      "ipv4": {
                                        "ipType": "STATIC",
                                        "dhcpRouteMetric": 1,
                                        "defaultRouteUsingDHCP": true,
                                        "type": "interfaceipv4",
                                        "ipAddress": {
                                          "standbyIpAddress": "",
                                          "type": "haipv4address",
                                          "netmask": "255.255.255.0",
                                          "ipAddress": "172.31.255.254"
                                        }
                                      },
                                      "name": "dmz-2",
                                 }
        ** Note ** See Api Browser for a complete data model and possible settings
        """
        return self.swagger_client.Interface.addSubInterface(body=sub_int_obj, parentId=parent_interface_id).result()

    @FTDAPIWrapper()
    def update_sub_interface(self, parent_interface_id: str, sub_int_obj: dict) -> dict:
        return self.swagger_client.Interface.editSubInterface(
            parentId=parent_interface_id, body=sub_int_obj, objId=sub_int_obj.id
        ).result()

    @FTDAPIWrapper()
    def delete_sub_interface(self, parent_interface_id: str, sub_interface_id: str) -> None:
        """Given a parentId (physical interface object id) and a sub interface id, delete this sub-interface config"""
        return self.swagger_client.Interface.deleteSubInterface(
            parentId=parent_interface_id, objId=sub_interface_id
        ).result()

    ################################
    # All Interface Objects (Read Only Calls!)

    @FTDAPIWrapper()
    def get_interface_operational_status_list(
        self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        """
        Get a list of the operational status and information for all interfaces
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of InterfaceData objects
        :rtype: list
        """
        return (
            self.swagger_client.Interface.getInterfaceDataList(limit=limit, offset=offset, filter=filter).result().items
        )

    @FTDAPIWrapper()
    def get_interface_operational_status(self, interface_id: str) -> dict:
        """
        Get the operational status and information for a specific interface, given the interface id
        :param interface_id: str interface object id for which we wish to retrieve data
        """
        return self.swagger_client.Interface.getInterfaceData(objId=interface_id).result()

    @FTDAPIWrapper()
    def get_interface_info_list(self) -> list:
        """
        This method is best used for learning what interfaces are present in the chassis and their capabilities.
        For example, Are SFP or modules are populated and if so with what capabilities
        :param interface_id: str optional interface ID
        """
        return self.swagger_client.InterfaceInfo.getInterfaceInfo(objId="default").result().interfaceInfoList