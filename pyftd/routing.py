import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDRouting:
    ################################
    # VRFs

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

    # TODO: Add VFR Create, Update, Delete Operations

    @FTDAPIWrapper()
    def get_static_routes(
        self, parentId="default", limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        """
        Get static routes. Note that this returns object names and not IP strings. So a subsequent call to
        get_network_objects() will probably be desired.
        :return: all static routes defined on the device
        :rtype: list of StaticRouteEntryWrapper
        """
        if self.api_version > 4:
            return (
                self.swagger_client.Routing.getStaticRouteEntryList(
                    parentId=parentId, limit=limit, offset=offset, filter=filter
                )
                .result()
                .items
            )
