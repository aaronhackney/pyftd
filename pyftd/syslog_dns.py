import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDSyslogDNSObjects:
    #############################
    # DNSGroup Objects
    @FTDAPIWrapper()
    def get_dnsgroup_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Return a list of DNS server configurations on this device.
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of DNSServerGroup objects
        :rtype: list
        """
        return self.swagger_client.DNS.getDNSServerGroupList(limit=limit, offset=offset, filter=filter).result().items

    @FTDAPIWrapper()
    def get_dnsgroup_object(self, dns_grp_obj_id: str) -> dict:
        """
        Return a dnsgroup object given a dnsGrouObject id
        """
        return self.swagger_client.DNS.getDNSServerGroup(objId=dns_grp_obj_id).result()

    @FTDAPIWrapper()
    def create_dnsgroup_object(self, dns_server_group_obj: dict) -> dict:
        """
        Add a DNSServerGroup object
        :param dns_server_group_obj: dict {
                                            "name": "My-Umbrella-Ella-Ella",
                                            "dnsServers":[
                                                {"ipAddress":"208.67.222.222","type":"dnsserver"},
                                                {"ipAddress":"208.67.220.220","type":"dnsserver"}
                                            ],
                                            "timeout": 2,
                                            "retries": 2,
                                            "searchDomain": "hacksbrain.com",
                                            "type": "dnsservergroup",
                                           }
        :return: dict DNSServerGroup object
        :rtype: dict DNSServerGroupWrapper
        """
        return self.swagger_client.DNS.addDNSServerGroup(body=dns_server_group_obj).result()

    def edit_dnsgroup_object(self, dns_server_group_obj: dict) -> dict:
        """
        Add a DNSServerGroup object
        :param dns_server_group_obj: dict
        :return: dict DNSServerGroup object
        :rtype: dict DNSServerGroupWrapper
        """
        return self.swagger_client.DNS.editDNSServerGroup(
            body=dns_server_group_obj, objId=dns_server_group_obj.id
        ).result()

    @FTDAPIWrapper()
    def delete_dnsgroup_object(self, dns_grp_obj_id: str) -> dict:
        """
        Delete a dnsgroup object given a dnsGrouObject id
        """
        return self.swagger_client.DNS.deleteDNSServerGroup(objId=dns_grp_obj_id).result()

    #############################
    # Syslog Server Objects
    @FTDAPIWrapper()
    def get_syslog_server_object_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Returns a list of syslog server objects.
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: str  The syslog server for which we wish to search for like "name:1.1.1.1:514" or "fts~1.1.1.1"
        :return: list of SyslogServerWrapper objects
        :rtype: list
        """
        return (
            self.swagger_client.SyslogServer.getSyslogServerList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_syslog_server_object(self, syslog_obj_id: str) -> dict:
        """
        Returns a syslog server object given an object id
        :param syslog_obj_id: str
        :return: dict SyslogServerWrapper object
        :rtype: dict SyslogServerWrapper object
        """
        return self.swagger_client.SyslogServer.getSyslogServer(objId=syslog_obj_id).result()

    @FTDAPIWrapper()
    def create_syslog_server_object(self, syslog_obj: dict) -> dict:
        """
        Add a syslog server object
        :param syslog_obj: dict {
                                    "name": "ElkStack",
                                    "deviceInterface": <interface_object>,
                                    "useManagementInterface": True,
                                    "protocol": "UDP",
                                    "host": "172.30.4.100",
                                    "port": "514",
                                    "type": "syslogserver",
                                }
        :return: dict SyslogServer object
        :rtype: dictSyslogServerWrapper

        Note: deviceInterface:

        Allowed Int Types=[BridgeGroupInterface, EtherChannelInterface, PhysicalInterface, SubInterface, VlanInterface]
        Only required if useManagementInterface=False - Should be an interface object
        """
        return self.swagger_client.SyslogServer.addSyslogServer(body=syslog_obj).result()

    @FTDAPIWrapper()
    def edit_syslog_server_object(self, syslog_obj: dict) -> dict:
        """
        Add a syslog server object
        :param syslog_obj: dict SyslogServer object
        :return: dict SyslogServer object
        :rtype: dictSyslogServerWrapper
        """
        return self.swagger_client.SyslogServer.editSyslogServer(body=syslog_obj, objId=syslog_obj.id).result()

    @FTDAPIWrapper()
    def delete_syslog_server_object(self, syslog_obj_id: str) -> dict:
        """
        Delete a syslog server object given an object id
        :param syslog_obj_id: str
        """
        return self.swagger_client.SyslogServer.deleteSyslogServer(objId=syslog_obj_id).result()
