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

    #########

    @FTDAPIWrapper()
    def get_secret_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of Secret objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return self.swagger_client.Secret.getSecretList(limit=limit, offset=offset, filter=filter).result().items

    @FTDAPIWrapper()
    def get_secret_object(self, secret_obj_id):
        """
        Get a specific secret object
        :param secret_obj_id: uuid of secret object
        :return: SecretWrapper
        """
        return self.swagger_client.Secret.getSecret(objId=secret_obj_id)

    @FTDAPIWrapper()
    def create_secret_object(self, secret_name, password, description=""):
        """
        Create a secret object
        :param secret_name: str name of the secret
        :param password: str the secrete password we wish to store
        :param description: str description of the secret
        :return: Secret object
        :rtype: SecretWrapper
        """
        secret_obj = {
            "name": secret_name,
            "password": password,
            "description": description,
            "type": "secret",
        }
        return self.swagger_client.Secret.addSecret(body=secret_obj).result()

    @FTDAPIWrapper()
    def get_radius_identity_source_list(self, limit=9999, offset=0, filter=""):
        """
        Get a list of Radius servers
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of RadiusIdentitySource objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.RadiusIdentitySource.getRadiusIdentitySourceList(
                limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def create_radius_identity_source(self, radius_obj):
        """
        Add a radius server
        :param radius_obj: RadiusIdentitySource object
        :return: RadiusIdentitySource object
        :rtype: RadiusIdentitySourceWrapper
        """
        return self.swagger_client.RadiusIdentitySource.addRadiusIdentitySource(body=radius_obj).result()

    @FTDAPIWrapper()
    def get_radius_identity_source_group_list(self, limit=9999, offset=0, filter=""):
        """
        Get a list of radius server groups
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of RadiusIdentitySourceGroup objects
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.RadiusIdentitySourceGroup.getRadiusIdentitySourceGroupList(
                limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def create_radius_identity_source_group(self, radius_group_obj):
        """
        Create a new radius group of servers
        :param radius_group_obj: RadiusIdentitySourceGroup object
        :return: RadiusIdentitySourceGroup object
        :rtype: RadiusIdentitySourceGroupWrapper
        """
        return self.swagger_client.RadiusIdentitySourceGroup.addRadiusIdentitySourceGroup(
            body=radius_group_obj
        ).result()

    #    @FTDAPIWrapper()
    #    def get_port_object_by_name(self, port_obj_name):
    #        """
    #        Search for a port object by name without specifying what kind of port (icmp, udp, tcp)
    #        :param port_obj_name:
    #        :return: TCPPortObject or UDPPortObject or ICMPv4Object or None
    #        """
    #        tcp_port_obj_list = self.get_tcp_port_object_list(filter=f"name:{port_obj_name}")
    #        if tcp_port_obj_list:
    #            return tcp_port_obj_list[0]
    #        else:
    #            udp_port_obj_list = self.get_udp_port_object_list(filter=f"name:{port_obj_name}")
    #            if udp_port_obj_list:
    #                return udp_port_obj_list[0]
    #            else:
    #                icmp_object_list = self.get_icmpv4_port_object_list(filter=f"name:{port_obj_name}")
    #                if icmp_object_list:
    #                    return icmp_object_list[0]
    #        return

    @FTDAPIWrapper()
    def get_dnsgroup_objects_list(self, filter="", limit=9999, offset=0):
        """
        Return a list of DNS server configurations on this device.
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of DNSServerGroup objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return self.swagger_client.DNS.getDNSServerGroupList(limit=limit, offset=offset, filter=filter).result().items

    @FTDAPIWrapper()
    def create_dnsgroup(self, dns_server_group_obj):
        """
        Add a DNSServerGroup object
        :param dns_server_group_obj: DNSServerGroup object
        :return: DNSServerGroup object
        :rtype: DNSServerGroupWrapper
        """
        return self.swagger_client.DNS.addDNSServerGroup(body=dns_server_group_obj).result()

    @FTDAPIWrapper()
    def get_syslog_server_object_list(self, limit=9999, offset=0, filter="") -> list:
        """
        Returns a list of syslog server objects.
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param search: str  The syslog server for which we wish to search for like "name:1.1.1.1:514" or "fts~1.1.1.1"
        :return: list of SyslogServerWrapper objects
        :rtype: list
        """
        if ":" in filter and not filter.split(":")[1]:  # a search key was provided with no value to search on
            return None
        return (
            self.swagger_client.SyslogServer.getSyslogServerList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def create_syslog_server_object(self, syslog_obj):
        """
        Add a syslog server object
        :param syslog_obj: SyslogServer object
        :type syslog_obj: SyslogServerWrapper
        :return: SyslogServer object
        :rtype: SyslogServerWrapper
        """
        syslog_obj["protocol"] = syslog_obj["protocol"].upper()
        return self.swagger_client.SyslogServer.addSyslogServer(body=syslog_obj).result()
