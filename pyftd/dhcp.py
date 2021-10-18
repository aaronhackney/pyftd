import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDDHCP:
    @FTDAPIWrapper()
    def get_dhcp_relay_services(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        return (
            self.swagger_client.DHCPRelayService.getDHCPRelayServiceList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    def get_dhcp_relay_service(self, dhcp_relay_svc_obj_id) -> list:
        return self.swagger_client.DHCPRelayService.getDHCPRelayService(objId=dhcp_relay_svc_obj_id).result()

    def update_dhcp_relay_service(self, dhcp_relay_svc_obj) -> list:
        # dhcp_relay_svc_obj
        # {
        #   "ipv4RelayTimeout": 0,
        #   "servers": [
        #     {
        #       "server": [network object],
        #       "interface": [interface object],
        #       "type": "dhcprelayserver"
        #     }
        #   ],
        #   "agents": [
        #     {
        #       "enableIpv4Relay": true,
        #       "setRoute": true,
        #       "interface": [interface object],
        #       "type": "dhcprelayagent"
        #     }
        #   ],
        #   "id": "string",
        #   "type": "dhcprelayservice"
        # }
        return self.swagger_client.DHCPRelayService.editDHCPRelayService(
            objId=dhcp_relay_svc_obj.id, body=dhcp_relay_svc_obj
        ).result()
