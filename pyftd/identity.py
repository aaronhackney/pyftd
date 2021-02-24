import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDIdentityObjects:
    #####################
    #  Radius Object
    @FTDAPIWrapper()
    def get_radius_identity_source_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get a list of Radius servers
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of RadiusIdentitySource objects
        :rtype: list
        """
        return (
            self.swagger_client.RadiusIdentitySource.getRadiusIdentitySourceList(
                limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_radius_identity_source(self, radius_src_obj_id: str) -> dict:
        """
        Given an object ID, return the RadiusIdentitySource object
        """
        return self.swagger_client.RadiusIdentitySource.getRadiusIdentitySource(objId=radius_src_obj_id).result()

    @FTDAPIWrapper()
    def create_radius_identity_source(self, radius_obj: dict) -> dict:
        """
        Add a radius server
        :param radius_obj: dict {
                                    "name":" "MY_RADIUS_10.10.10.111",
                                    "description": "Radius server at 10.10.10.111",
                                    "host": "10.10.10.111",
                                    "capabilities": ['AUTHENTICATION', 'AUTHORIZATION', 'ACCOUNTING',
                                                   'DIRECTORY_SERVICES', 'PASSIVE_IDENTITY'],
                                    "timeout": 2,
                                    "serverAuthenticationPort": 1812,
                                    "serverSecretKey": "abc123",
                                    "useRoutingToSelectInterface": True,
                                    "redirectAcl": <ExtendedAccessList Object>
                                    "interface": <Interface Object> (Only if useRoutingToSelectInterface: False)
                                    "type": "radiusidentitysource",
                                }
        :return: dict RadiusIdentitySource object
        :rtype: dict RadiusIdentitySourceWrapper
        """
        return self.swagger_client.RadiusIdentitySource.addRadiusIdentitySource(body=radius_obj).result()

    @FTDAPIWrapper()
    def edit_radius_identity_source(self, radius_obj: dict) -> dict:
        """
        Add a radius server
        :param radius_obj: dict  RadiusIdentitySource object
        :return: dict RadiusIdentitySource object
        :rtype: dict RadiusIdentitySourceWrapper
        """
        return self.swagger_client.RadiusIdentitySource.editRadiusIdentitySource(
            body=radius_obj, objId=radius_obj.id
        ).result()

    @FTDAPIWrapper()
    def delete_radius_identity_source(self, radius_src_obj_id: str) -> None:
        """
        Given an object ID, delete the RadiusIdentitySource object
        """
        return self.swagger_client.RadiusIdentitySource.deleteRadiusIdentitySource(objId=radius_src_obj_id).result()

    ######################
    #  Radius Group Object
    @FTDAPIWrapper()
    def get_radius_identity_source_group_list(
        self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> None:
        """
        Get a list of radius server groups
        :param limit: limit the number of records returned
        :param offset: starting index of records to return (for paging)
        :param filter: limit returned results based on filters like "name:foo" or "fts~bar"
        :return: list of RadiusIdentitySourceGroup objects
        """
        return (
            self.swagger_client.RadiusIdentitySourceGroup.getRadiusIdentitySourceGroupList(
                limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_radius_identity_source_group(self, radius_src_grp_id: str) -> dict:
        """
        Given an object ID, return the RadiusIdentitySourceGroup object
        """
        return self.swagger_client.RadiusIdentitySourceGroup.getRadiusIdentitySourceGroup(
            objId=radius_src_grp_id
        ).result()

    @FTDAPIWrapper()
    def create_radius_identity_source_group(self, radius_group_obj: dict) -> dict:
        """
        Create a new radius group of servers
        :param radius_group_obj: dict {
                                        "name": "MYRADIUS",
                                        "description": "MY RADIUS GROUP",
                                        "deadTime": 5,
                                        "maxFailedAttempts": 3,
                                        "radiusIdentitySources": [radius_ident_obj_1, radius_ident_obj_2],
                                        "activeDirectoryRealm": ActiveDirectoryRealm_obj,
                                        "enableDynamicAuthorization": true,
                                        "dynamicAuthorizationPort": 0,
                                        "type": "radiusidentitysourcegroup"
                                      }
        :param radius_group_obj: RadiusIdentitySourceGroup object
        :return: dict RadiusIdentitySourceGroup object
        :rtype: dict RadiusIdentitySourceGroupWrapper
        """
        return self.swagger_client.RadiusIdentitySourceGroup.addRadiusIdentitySourceGroup(
            body=radius_group_obj
        ).result()

    @FTDAPIWrapper()
    def edit_radius_identity_source_group(self, radius_group_obj: dict) -> dict:
        """
        Edit an existing radius group of servers
        :param radius_group_obj: dict
        :return: dict RadiusIdentitySourceGroup object
        :rtype: dict RadiusIdentitySourceGroupWrapper
        """
        return self.swagger_client.RadiusIdentitySourceGroup.editRadiusIdentitySourceGroup(
            body=radius_group_obj, objId=radius_group_obj.id
        ).result()

    @FTDAPIWrapper()
    def delete_radius_identity_source_group(self, radius_src_grp_id: str) -> None:
        """
        Given an object ID, delete the RadiusIdentitySourceGroup object
        """
        return self.swagger_client.RadiusIdentitySourceGroup.deleteRadiusIdentitySourceGroup(
            objId=radius_src_grp_id
        ).result()
