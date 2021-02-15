import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDPortObjects:
    @FTDAPIWrapper()
    def get_tcp_port_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get a list of tcp port objects
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of TCPPortObject objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.PortObject.getTCPPortObjectList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_tcp_port_object(self, tcp_port_obj_id: str) -> dict:
        """
        Given an objectId, return the tcp port object
        :param tcp_port_obj_id: str
        """
        return self.swagger_client.PortObject.getTCPPortObject(objId=tcp_port_obj_id).result()

    @FTDAPIWrapper()
    def create_tcp_port_object(self, tcp_port_obj: dict) -> dict:
        """
        :param tcp_port_obj" dict {
                                    "name":"test",
                                    "description":"test",
                                    "port":"25",
                                    "type":"tcpportobject"
                                  }
        :return: tcpportobject
        :rtype: TCPPortObjectWrapper
        """
        return self.swagger_client.PortObject.addTCPPortObject(body=tcp_port_obj).result()

    @FTDAPIWrapper()
    def edit_tcp_port_object(self, tcp_port_obj: dict) -> dict:
        return self.swagger_client.PortObject.editTCPPortObject(body=tcp_port_obj, objId=tcp_port_obj.id).result()

    @FTDAPIWrapper()
    def delete_tcp_port_object(self, port_obj_id: str) -> None:
        """
        Delete a tcp port object
        :param port_obj_id: uuid of the tcp port object
        :return: none
        """
        return self.swagger_client.PortObject.deleteTCPPortObject(objId=port_obj_id).result()

    ##########

    @FTDAPIWrapper()
    def get_port_object_group_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get a list of port object groups
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of PortObjectGroup objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.PortObject.getPortObjectGroupList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_icmpv4_port_object_list(self, limit=9999, offset=0, filter=""):
        """
        Get a list of ipv4 icmp port objects
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of ipv4 icmp port objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.PortObject.getICMPv4PortObjectList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_udp_port_object_list(self, limit=9999, offset=0, filter=""):
        """
        Get a list of udp port objects
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of UDPPortObject objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.PortObject.getUDPPortObjectList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def delete_udp_port_object(self, port_obj_id):
        """
        Delete a udp port object
        :param port_obj_id: uuid of the udp port object
        :return: none
        """
        return self.swagger_client.PortObject.deleteUDPPortObject(objId=port_obj_id).result()

    @FTDAPIWrapper()
    def delete_icmp_port_object(self, port_obj_id):
        """
        Delete a ipv4 icmp port object
        :param port_obj_id: uuid of the ipv4 icmp port object
        :return: none
        """
        return self.swagger_client.PortObject.deleteICMPv4PortObject(objId=port_obj_id).result()

    @FTDAPIWrapper()
    def create_udp_port_object(self, name, port, description=""):
        """
        Create a UDP port object
        :param name: str name of the port object
        :param port: str the udp port number
        :param description: str description of the udp port
        :return: UDPPortObject object
        :rtype: UDPPortObjectWrapper
        """
        udp_port_object = {
            "name": name,
            "port": port,
            "type": "udpportobject",
            "description": description,
        }
        return self.swagger_client.PortObject.addUDPPortObject(body=udp_port_object).result()

    @FTDAPIWrapper()
    def create_icmpv4_port_object(self, name, icmpv4type, icmpv4code="", description=""):
        """
        Create an ipv4 icmp port object
        :param name: str name of the ipv4 icmp port object
        :param icmpv4type: str the icmp type to create ['ANY', 'ECHO_REPLY', 'DESTINATION_UNREACHABLE', 'SOURCE_QUENCH',
         'REDIRECT_MESSAGE', 'ALTERNATE_HOST_ADDRESS', 'ECHO_REQUEST', 'ROUTER_ADVERTISEMENT', 'ROUTER_SOLICITATION',
         'TIME_EXCEEDED', 'PARAMETER_PROBLEM', 'TIMESTAMP', 'TIMESTAMP_REPLY', 'INFO_REQUEST', 'INFO_REPLY',
         'ADDR_MASK_REQUEST', 'ADDR_MASK_REPLY', 'TRACEROUTE', 'DATAGRAM_CONVERSION_ERROR', 'MOBILE_HOST_REDIRECT',
         'WHERE_ARE_YOU', 'HERE_I_AM', 'MOBILE_REG_REQUEST', 'MOBILE_REG_REPLY', 'DOMAIN_NAME_REQUEST',
         'DOMAIN_NAME_REPLY', 'SKIP_ALGORITHM_DISCOVERY_PROTOCOL', 'PHOTURIS', 'EXPERIMENTAL_MOB_PROTOCOLS']
        :param icmpv4code: str the icmp code to create (less common) ['ANY_IPV4', 'NET_UNREACHABLE', 'HOST_UNREACHABLE',
         'PROTOCOL_UNREACHABLE', 'PORT_UNREACHABLE', 'FRAGMENTATION_NEEDED', 'SOURCE_ROUTE_FAILED',
         'DEST_NETWORK_UNKNOWN', 'DEST_HOST_UNKNOWN', 'SRC_HOST_ISOLATED', 'COMMUNICATION_DEST_NET_PROHIBITED',
         'COMMUNICATION_DEST_HOST_PROHIBITED', 'DEST_NET_UNREACHABLE_FOR_TOS', 'DEST_HOST_UNREACHABLE_FOR_TOS',
         'COMM_ADMINISTRATIVELY_PROHIBITED', 'HOST_PRECEDENCE_VIOLATION', 'PRECEDENCE_CUTOFF',
         'REDIRECT_DATAGRAM_NETWORK', 'REDIRECT_DATAGRAM_HOST', 'REDIRECT_DATAGRAM_SERVICE_NETWORK',
         'REDIRECT_DATAGRAM_SERVICE_HOST', 'ALTERNATE_HOST_ADDR', 'NORMAL_ROUTER_ADV', 'DO_NOT_ROUTE_COMMON_TRAFFIC',
         'TTL_EXPIRED_TRANSIT', 'FRAG_ASSEMBLY', 'PTR_ERROR', 'MISSING_REQD_OPTION', 'BAD_LENGTH', 'BAD_SPI',
         'AUTH_FAILED', 'DECOMPRESSION_FAILED', 'DECRYPTION_FAILED', 'NEED_AUTHENTICATION', 'NEED_AUTHORIZATION']
        :param description: str description of the udp port
        :return: UDPPortObject object
        :rtype: UDPPortObjectWrapper
        """
        if icmpv4code != "":
            icmpv4_port_object = {
                "name": name,
                "icmpv4Type": icmpv4type,
                "type": "icmpv4portobject",
                "icmpv4Code": icmpv4code,
                "description": description,
            }
        else:
            icmpv4_port_object = {
                "name": name,
                "icmpv4Type": icmpv4type,
                "type": "icmpv4portobject",
                "description": description,
            }
        return self.swagger_client.PortObject.addICMPv4PortObject(body=icmpv4_port_object).result()

    @FTDAPIWrapper()
    def create_port_object_group(self, obj_group_name, port_obj_list, description=""):
        """
        Create a port object group
        :param obj_group_name: str name of the port object group
        :param port_obj_list: list of objects [TCPPortObject, UDPPortObject, ProtocolObject, ICMPv4Object ICMPv6Object]
        :param description:
        :return:
        """
        return self.swagger_client.PortObject.addPortObjectGroup(
            body={
                "name": obj_group_name,
                "description": description,
                "objects": port_obj_list,
                "type": "portobjectgroup",
            }
        ).result()
