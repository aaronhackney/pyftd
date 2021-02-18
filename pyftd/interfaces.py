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
