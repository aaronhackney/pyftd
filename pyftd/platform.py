import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDPlatform:
    """
    Set platform and control plane settings hostname, syslog, ntp, aaa, systeminfo
    """

    ################################
    # NTP Settings
    #
    @FTDAPIWrapper()
    def get_ntp_servers_list(self):
        return self.swagger_client.NTP.getNTPList().result().items

    @FTDAPIWrapper()
    def edit_ntp_servers(self, ntp_servers_obj: dict) -> dict:
        return self.swagger_client.NTP.editNTP(objId=ntp_servers_obj.id, body=ntp_servers_obj).result()

    ################################
    # Syslog Settings
    #
    @FTDAPIWrapper()
    def get_hostname_list(self) -> list:
        """
        Get the platform hostname.
        :return: object that contains the platform hostname
        :rtype: list of DeviceHostnameWrapper
        """
        return self.swagger_client.DeviceHostname.getDeviceHostnameList().result().items

    @FTDAPIWrapper()
    def get_hostname(self, hostname_id: str) -> dict:
        """
        Get the platform hostname
        :param hostname_id: str id of hostname object
        :return: dict object that contains the platform hostname
        :rtype: dict of DeviceHostnameWrapper
        """
        return self.swagger_client.DeviceHostname.getDeviceHostnameList(objId=hostname_id).result()

    @FTDAPIWrapper()
    def edit_hostname(self, hostname_obj: dict) -> dict:
        """Set the platform hostname.
        :param hostname_obj: dict the hostname desired for the platform
        :return: dict that we applied to the configuration
        :rtype: dict DeviceHostnameWrapper
        """
        return self.swagger_client.DeviceHostname.editDeviceHostname(objId=hostname_obj.id, body=hostname_obj).result()

    ################################
    # Syslog Settings buffered, console, and remote
    #
    @FTDAPIWrapper()
    def get_device_log_settings_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        return (
            self.swagger_client.DeviceLogSettings.getDeviceLogSettingsList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_device_log_setting(self):
        pass

    @FTDAPIWrapper()
    def add_device_log_settings(self):
        pass

    @FTDAPIWrapper()
    def edit_device_log_settings(self, log_settings_obj):
        return self.swagger_client.DeviceLogSettings.editDeviceLogSettings(
            objId=log_settings_obj.id, body=log_settings_obj
        ).result()

    @FTDAPIWrapper()
    def delete_device_log_settings(self, log_settings_obj_id):
        pass

    ################################
    # Management DNS Settings
    #
    @FTDAPIWrapper()
    def get_mgmt_dns_settings_list(self):
        return self.swagger_client.DNS.getDeviceDNSSettingsList().result().items

    @FTDAPIWrapper()
    def edit_mgmt_dns_settings(self, dns_settings):
        return self.swagger_client.DNS.editDeviceDNSSettings(objId=dns_settings.id, body=dns_settings).result()

    ################################
    # Data Interface DNS Settings
    #
    @FTDAPIWrapper()
    def get_data_dns_settings_list(self):
        return self.swagger_client.DNS.getDataDNSSettingsList().result().items

    @FTDAPIWrapper()
    def edit_data_dns_settings(self, dns_settings):
        return self.swagger_client.DNS.editDataDNSSettings(objId=dns_settings.id, body=dns_settings).result()

    @FTDAPIWrapper()
    def get_aaa_server_by_name(self, aaa_name):
        aaa_server_list = self.get_aaa_setting_list()
        for aaa_server in aaa_server_list:
            if aaa_server.name.lower() == aaa_name.lower():
                logger.debug(f"Found a matching aaa server by name {aaa_name}")
                return aaa_server

    ################################
    # Platform AAA Servers
    #
    @FTDAPIWrapper()
    def get_aaa_settings_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        return (
            self.swagger_client.AAASetting.getAAASettingList(limit=limit, offset=offset, filter=filter).result().items
        )

    @FTDAPIWrapper()
    def get_aaa_settings(self, aaa_obj_id: str) -> dict:
        return self.swagger_client.AAASetting.getAAASetting(objId=aaa_obj_id).result()

    @FTDAPIWrapper()
    def edit_aaa_settings(self, aaa_obj: dict) -> dict:
        return self.swagger_client.AAASetting.editAAASetting(objId=aaa_obj.id, body=aaa_obj).result()

    @FTDAPIWrapper()
    def delete_aaa_settings(self, aaa_obj_id: str) -> None:
        return self.swagger_client.AAASetting.deleteAAASetting(objId=aaa_obj_id).result()

    ################################
    # Misc read-only platform data
    #
    @FTDAPIWrapper()
    def get_system_information(self, obj_id="default") -> dict:
        """Get system information like hardware info, software version, vbd version, model, etc
        :param obj_id: str set to "default"
        :return: dict containing system information like hardware info, software version, vbd version, and model
        :rtype: dict SystemInformationWrapper
        """
        return self.swagger_client.SystemInformation.getSystemInformation(objId=obj_id).result()
