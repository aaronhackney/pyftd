import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDRouting:
    ################################
    # VRFs
    # TODO: Add VFR Create, Update, Delete Operations as of FTD 7.0 VRF is available with Snort 3.x
    @FTDAPIWrapper()
    def get_vrf_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get a list of VRFs configured on the appliance
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        """
        return (
            self.swagger_client.Routing.getVirtualRouterList(limit=limit, offset=offset, filter=filter).result().items
        )

    @FTDAPIWrapper()
    def get_vrf(self, vrf_id: str) -> dict:
        """
        Get a list of VRFs configured on the appliance
        :param vrf_id: str objext id of the vrf
        """
        return self.swagger_client.Routing.getVirtualRouter(objId=vrf_id).result()

    ################################
    # Static Routing

    @FTDAPIWrapper()
    def get_static_route_list(
        self, parent_id: str = "default", limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        """
        Get static routes from the given VRF (Global vrf parent_id = "default")
        :param parent_id: str the object id of the VRF from which we wish to get static routes
        :return: list all static routes defined on the device
        :rtype: list of StaticRouteEntryWrapper
        """
        return (
            self.swagger_client.Routing.getStaticRouteEntryList(
                parentId=parent_id, limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def create_static_route(self, route_obj: dict, parent_id: str = "default", at=None) -> dict:
        """
        Add a static route to the given VRF
        :param route_obj dict = {
                                    "description": "test adding static route",
                                    "metricValue": 1,
                                    "ipType": "IPv4",
                                    "type": "staticrouteentry",
                                    "name": "unittest-route",
                                    "networks": [ <network_object_1> <network_object_2>...],
                                    "gateway": <host object>
                                    "iface": <iface object>,
                                    "slaMonitor": <sla object>
                                }
        :param parent_id: str the object id of the VRF in which we wish to create a static route
        :param at: int the numeric order of where we want the route to be placed
        :return: dict of the static route
        :rtype: dict StaticRouteEntryWrapper
        """
        return self.swagger_client.Routing.addStaticRouteEntry(parentId=parent_id, body=route_obj, at=at).result()

    @FTDAPIWrapper()
    def edit_static_route(self, route_obj: dict, parent_id: str = "default", at=None) -> dict:
        """
        Modify a static route in the given VRF
        :param route_obj: dict static route
        :param parent_id: str the object id of the VRF in which we wish to edit a static route
        :param at: int the numeric order of where we want the route to be placed
        :return: dict of the static route
        :rtype: dict StaticRouteEntryWrapper
        """
        return self.swagger_client.Routing.editStaticRouteEntry(
            parentId=parent_id, body=route_obj, objId=route_obj.id, at=at
        ).result()

    @FTDAPIWrapper()
    def delete_static_route(self, route_obj_id: dict, parent_id: str = "default") -> None:
        """
        delete a static route from the given VRF
        :param route_obj_id: str the route object id
        :param parent_id: str the object id of the VRF from which we wish to delete the static route
        :return: dict of the static route
        :rtype: dict StaticRouteEntryWrapper
        """
        return self.swagger_client.Routing.deleteStaticRouteEntry(parentId=parent_id, objId=route_obj_id).result()

    ################################
    # SLA Monitors
    @FTDAPIWrapper()
    def get_sla_monitor_list(self) -> list:
        """
        Get list of sla monitor objects
        """
        self.swagger_client.SLAMonitor.getSLAMonitorList().result().items

    @FTDAPIWrapper()
    def get_sla_monitor(self, sla_monitor_id: str) -> dict:
        """
        Get sla monitor
        :param sla_monitor_id: str id of the monitor object
        """
        self.swagger_client.SLAMonitor.getSLAMonitor(objId=sla_monitor_id).result()

    @FTDAPIWrapper()
    def get_sla_monitor_status_list(self) -> list:
        """
        Get the current status of SLA monitors
        """
        return self.swagger_client.SLAMonitor.getSLAMonitorList().result().items

    @FTDAPIWrapper()
    def get_sla_monitor_status(self, sla_obj_id: str) -> dict:
        """
        Get the current status of a specific SLA monitor
        :param sla_monitor_id: str id of the monitor object
        """
        return self.ftd_client.swagger_client.SLAMonitor.getSLAMonitorStatus(objId=sla_obj_id).result().items

    @FTDAPIWrapper()
    def add_sla_monitor(self, sla_monitor: dict) -> dict:
        """
        :param sla_monitor: dict {
                                  "description": "Test SLA Monitor",
                                  "type": "slamonitor",
                                  "slaOperation": {
                                    "timeout": 5000,
                                    "frequency": 60000,
                                    "threshold": 5000,
                                    "numOfPackets": 1,
                                    "typeOfService": 0,
                                    "dataSize": 28,
                                    "type": "ipicmpecho"
                                  },
                                  "name": "TEST-SLA",
                                  "monitoredAddress": <network host object>,
                                  "targetInterface": <interface object>
                                }
        """
        return self.swagger_client.SLAMonitor.addSLAMonitor(body=sla_monitor).result()

    @FTDAPIWrapper()
    def edit_sla_monitor(self, sla_monitor: dict) -> dict:
        """
        :param sla_monitor: dict
        """
        return self.swagger_client.SLAMonitor.editSLAMonitor(body=sla_monitor, objId=sla_monitor.id).result()

    @FTDAPIWrapper()
    def delete_sla_monitor(self, sla_monitor_id: str) -> None:
        """
        Delete SLA object given the object id
        :param sla_monitor_id: str id of the monitor object
        """
        return self.swagger_client.SLAMonitor.deleteSLAMonitor(objId=sla_monitor_id).result()
