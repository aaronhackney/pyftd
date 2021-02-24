import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDNatPolicy:
    ################################
    # Autonat
    @FTDAPIWrapper()
    def get_autonat_container_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        Get the Autonat Container list - This will contain the parentId needed for other operations.
        :return: list of ObjectNatRuleContainerWrapper objects
        :rtype: list
        """
        return (
            self.swagger_client.NAT.getObjectNatRuleContainerList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_autonat_container(self, autonat_container_id) -> dict:
        """
        Get the Autonat Container list - get the autonat container(s) from which we will need a parentid for other calls
        :param autonat_container_id: str the container id we wish to retrieve
        :return: dict ObjectNatRuleContainerWrapper object
        :rtype: dict ObjectNatRuleContainerWrapper
        """
        return self.swagger_client.NAT.getObjectNatRuleContainerList(objId=autonat_container_id).result()

    @FTDAPIWrapper()
    def get_autonat_policy_list(
        self, autonat_parent_id, limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        return (
            self.swagger_client.NAT.getObjectNatRuleList(
                parentId=autonat_parent_id, limit=limit, offset=offset, filter=filter
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_autonat_policy(self, autonat_parent_id: str, nat_obj_id: str) -> dict:
        """
        Get a specific autonat config
        :param autonat_parent_id: str the container id of the before or after autonat container
        :param nat_obj_id: str the object id of the nat config we wish to retrieve
        :return: dict ObjectNatRuleWrapper object
        :rtype: dict ObjectNatRuleWrapper
        """
        return self.swagger_client.NAT.getObjectNatRule(parentId=autonat_parent_id, objId=nat_obj_id).result()

    @FTDAPIWrapper()
    def add_autonat_policy(self, autonat_parent_id: str, nat_policy: dict) -> dict:
        """
        Given a ManualNatRuleWrapper dict object- see create_manual_nat_object(), create the autonat rule as specified.
        :param autonat_parent_id: the autonat container (parentId)
        :param nat_policy: ObjectNatRuleWrapper (See model above)
        :return: dict ObjectNatRuleWrapper
        :rtype: dict ObjectNatRuleWrapper
        """
        return self.swagger_client.NAT.addObjectNatRule(parentId=autonat_parent_id, body=nat_policy).result()

    @FTDAPIWrapper()
    def edit_autonat_policy(self, autonat_parent_id: str, nat_policy: dict) -> dict:
        """
        Update an existing autonat
        :param autonat_parent_id: parentId of the autonat (from the autonatcontainer)
        :param nat_policy: the autonat we wish to modify
        :return: dict ObjectNatRule
        :rtype: dict ObjectNatRule
        """
        return self.swagger_client.NAT.editObjectNatRule(
            parentId=autonat_parent_id, objId=nat_policy.id, body=nat_policy
        ).result()

    @FTDAPIWrapper()
    def delete_autonat_policy(self, autonat_parent_id: str, nat_obj_id: str) -> None:
        """
        Delete a specific autonat config
        :param autonat_parent_id: str the container id of the before or after autonat container
        :param nat_obj_id: str the object id of the nat config we wish to retrieve
        :return: None
        """
        return self.swagger_client.NAT.deleteObjectNatRule(parentId=autonat_parent_id, objId=nat_obj_id).result()

    ################################
    # Manual Nat
    @FTDAPIWrapper()
    def get_manual_nat_container_list(self, limit: int = 9999, offset: int = 0, filter: Optional[str] = None) -> list:
        """
        This will return a ManualNatContainer list that contains 2 keys:
            Key 0: NGFW-After-Auto-NAT-Policy
            Key 1: NGFW-Before-Auto-NAT-Policy
        These are the parentIDs of the containers that wrap the before-auto-nat and after-auto-nat policies
        :return list of ManualNatContainerWrappera:
        :rtype: list
        """
        return (
            self.swagger_client.NAT.getManualNatRuleContainerList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_manual_nat_container(self, manual_nat_container_id: str) -> dict:
        """
        This will return a ManualNatContainer
        :return dict ManualNatContainerWrapper:
        :rtype: dict
        """
        return (
            self.swagger_client.NAT.getManualNatRuleContainerList(limit=limit, offset=offset, filter=filter)
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_manual_nat_policy_list(
        self, manual_nat_parent_id, limit: int = 9999, offset: int = 0, filter: Optional[str] = None
    ) -> list:
        """
        :param manual_nat_parent_id: str the object id of the manaul nat container (beforenat or afternat container)
        :return: list of manual nat policies
        :rtype: list
        """
        return (
            self.swagger_client.NAT.getManualNatRuleList(
                parentId=manual_nat_parent_id, filter=search, offset=offset, limit=limit
            )
            .result()
            .items
        )

    @FTDAPIWrapper()
    def get_manual_nat_policy(self, manual_nat_parent_id: str, nat_obj_id):
        """
        Get a specific Manual NAT object
        :param manual_nat_parent_id: str the object id of the manaul nat container (beforenat or afternat container)
        :param nat_obj_id: str The ManualNatRuleWrapper object id that we wish to get
        :return: dict  ManualNatRuleWrapper
        :rtype: dict ManualNatRuleWrapper
        """
        return self.swagger_client.NAT.getManualNatRule(parentId=manual_nat_parent_id, objId=nat_obj_id).result()

    @FTDAPIWrapper()
    def add_manual_nat_policy(self, manual_nat_parent_id: str, nat_policy_obj: dict) -> dict:
        """
        Create a manual nat, either before autonat or after autonat, depending on the manual_nat_parent_id
        :param manual_nat_parent_id: str the object id of the manaul nat container (beforenat or afternat container)
        :param nat_policy_obj: dict the manual nat we wish to create
        :return: dict  ManualNatRuleWrapper
        :rtype: dict ManualNatRuleWrapper
        """
        return self.swagger_client.NAT.addManualNatRule(parentId=manual_nat_parent_id, body=nat_policy_obj).result()

    @FTDAPIWrapper()
    def edit_manual_nat_policy(self, manual_nat_parent_id, nat_policy_obj):
        """
        :param manual_nat_parent_id: str the object id of the manaul nat container (beforenat or afternat container)
        :param nat_policy_obj: dict the manual nat we wish to create
        :return: dict  ManualNatRuleWrapper
        :rtype: dict ManualNatRuleWrapper
        """
        return self.swagger_client.NAT.editManualNatRule(
            parentId=manual_nat_parent_id, objId=nat_policy_obj.id, body=nat_policy_obj
        ).result()

    @FTDAPIWrapper()
    def delete_manual_nat_policy(self, manual_nat_parent_id: str, nat_obj_id: str) -> None:
        """
        Delete a specific Manual NAT object
        :param manual_nat_parent_id: str the object id of the manaul nat container (beforenat or afternat container)
        :param nat_obj_id: str The ManualNatRuleWrapper object id that we wish to delete
        :return: None
        """
        return self.swagger_client.NAT.getManualNatRule(parentId=manual_nat_parent_id, objId=nat_obj_id).result()
