from typing import Any, Dict

from ....action.mixins.archived_meeting_check_mixin import CheckForArchivedMeetingMixin
from ....models.models import User
from ....permissions.management_levels import (
    CommitteeManagementLevel,
    OrganizationManagementLevel,
)
from ....permissions.permission_helper import (
    has_committee_management_level,
    has_organization_management_level,
    has_perm,
)
from ....permissions.permissions import Permissions
from ....shared.exceptions import PermissionDenied
from ....shared.patterns import Collection, FullQualifiedId
from ....shared.schema import required_id_schema
from ...generics.update import UpdateAction
from ...util.default_schema import DefaultSchema
from ...util.register import register_action
from ...util.typing import ActionData


@register_action("user.set_present")
class UserSetPresentAction(UpdateAction, CheckForArchivedMeetingMixin):
    """
    Action to set present.
    """

    model = User()
    schema = DefaultSchema(User()).get_update_schema(
        additional_required_fields={
            "present": {"type": "boolean"},
            "meeting_id": required_id_schema,
        }
    )

    def get_updated_instances(self, action_data: ActionData) -> ActionData:
        """
        update is_present_in_meeting_ids:
        add meeting_id if present is True.
        remove meeting_id if present is False.
        """
        for instance in action_data:
            meeting_id = instance.pop("meeting_id")
            present = instance.pop("present")
            user = self.datastore.get(
                FullQualifiedId(self.model.collection, instance["id"]),
                ["is_present_in_meeting_ids"],
            )
            if present:
                if meeting_id not in user.get("is_present_in_meeting_ids", []):
                    instance["is_present_in_meeting_ids"] = user.get(
                        "is_present_in_meeting_ids", []
                    ) + [meeting_id]
                    yield instance
            elif present is False:
                is_present = user.get("is_present_in_meeting_ids", [])
                if meeting_id in is_present:
                    is_present.remove(meeting_id)
                    instance["is_present_in_meeting_ids"] = is_present
                    yield instance

    def check_permissions(self, instance: Dict[str, Any]) -> None:
        if has_organization_management_level(
            self.datastore, self.user_id, OrganizationManagementLevel.CAN_MANAGE_USERS
        ):
            return
        if has_perm(
            self.datastore,
            self.user_id,
            Permissions.User.CAN_MANAGE_PRESENCE,
            instance["meeting_id"],
        ):
            return
        meeting = self.datastore.get(
            FullQualifiedId(Collection("meeting"), instance["meeting_id"]),
            ["committee_id", "users_allow_self_set_present"],
        )
        if has_committee_management_level(
            self.datastore,
            self.user_id,
            CommitteeManagementLevel.CAN_MANAGE,
            meeting["committee_id"],
        ):
            return
        if self.user_id == instance["id"] and meeting.get(
            "users_allow_self_set_present"
        ):
            return
        raise PermissionDenied("You are not allowed to set present.")
