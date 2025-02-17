import time
from typing import Any, Dict

from ....models.models import Motion
from ....permissions.permission_helper import has_perm
from ....permissions.permissions import Permissions
from ....shared.exceptions import ActionException, PermissionDenied
from ....shared.patterns import Collection, FullQualifiedId
from ...util.default_schema import DefaultSchema
from ...util.register import register_action
from ..user.create import UserCreate
from ..user.update import UserUpdate
from .create_base import MotionCreateBase
from .update_all_derived_motion_ids import MotionUpdateAllDerivedMotionIds


@register_action("motion.create_forwarded")
class MotionCreateForwarded(MotionCreateBase):
    """
    Create action for forwarded motions.
    """

    schema = DefaultSchema(Motion()).get_create_schema(
        optional_properties=[
            "reason",
        ],
        required_properties=["meeting_id", "title", "text", "origin_id"],
    )

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        meeting = self.datastore.get(
            FullQualifiedId(Collection("meeting"), instance["meeting_id"]),
            [
                "motions_default_workflow_id",
            ],
        )
        self.set_state_from_workflow(instance, meeting)
        committee = self.check_for_origin_id(instance)
        self.check_state_allow_forwarding(instance)

        # handle forwarding user
        target_meeting = self.datastore.get(
            FullQualifiedId(Collection("meeting"), instance["meeting_id"]),
            ["id", "default_group_id"],
        )
        if committee.get("forwarding_user_id"):
            forwarding_user_id = committee["forwarding_user_id"]
            forwarding_user = self.datastore.get(
                FullQualifiedId(Collection("user"), forwarding_user_id),
                [f"group_${instance['meeting_id']}_ids"],
            )
            if target_meeting["default_group_id"] not in forwarding_user.get(
                f"group_${instance['meeting_id']}_ids", []
            ):
                user_update_payload = [
                    {
                        "id": forwarding_user_id,
                        "group_$_ids": {
                            str(instance["meeting_id"]): forwarding_user.get(
                                f"group_${instance['meeting_id']}_ids", []
                            )
                            + [target_meeting["default_group_id"]]
                        },
                    }
                ]
                self.execute_other_action(UserUpdate, user_update_payload)
        else:
            committee_user_create_payload = {
                "username": committee.get("name", "Committee User"),
                "is_physical_person": False,
                "is_active": False,
                "group_$_ids": {
                    str(target_meeting["id"]): [target_meeting["default_group_id"]]
                },
                "forwarding_committee_ids": [committee["id"]],
            }
            action_result = self.execute_other_action(
                UserCreate, [committee_user_create_payload]
            )
            assert action_result and action_result[0]
            forwarding_user_id = action_result[0]["id"]
        instance["submitter_ids"] = [forwarding_user_id]

        self.create_submitters(instance)
        self.set_sequential_number(instance)
        self.set_created_last_modified_and_number(instance)
        self.calculate_all_origin_ids_and_all_derived_motion_ids(instance)
        instance["forwarded"] = round(time.time())
        return instance

    def check_for_origin_id(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        meeting = self.datastore.get(
            FullQualifiedId(Collection("meeting"), instance["meeting_id"]),
            ["committee_id"],
        )
        forwarded_from = self.datastore.get(
            FullQualifiedId(Collection("motion"), instance["origin_id"]),
            ["meeting_id"],
        )
        forwarded_from_meeting = self.datastore.get(
            FullQualifiedId(Collection("meeting"), forwarded_from["meeting_id"]),
            ["committee_id"],
        )
        # use the forwarding user id and id later in the handle forwarding user
        # code.
        committee = self.datastore.get(
            FullQualifiedId(
                Collection("committee"), forwarded_from_meeting["committee_id"]
            ),
            ["id", "name", "forward_to_committee_ids", "forwarding_user_id"],
        )
        if meeting["committee_id"] not in committee.get("forward_to_committee_ids", []):
            raise ActionException(
                f"Committee id {meeting['committee_id']} not in {committee.get('forward_to_committee_ids', [])}"
            )
        return committee

    def check_permissions(self, instance: Dict[str, Any]) -> None:
        origin = self.datastore.get(
            FullQualifiedId(self.model.collection, instance["origin_id"]),
            ["meeting_id"],
        )
        perm_origin = Permissions.Motion.CAN_FORWARD
        if not has_perm(
            self.datastore, self.user_id, perm_origin, origin["meeting_id"]
        ):
            msg = f"You are not allowed to perform action {self.name}."
            msg += f" Missing permission: {perm_origin}"
            raise PermissionDenied(msg)

        # check if origin motion is amendment or statute_amendment
        origin = self.datastore.get(
            FullQualifiedId(self.model.collection, instance["origin_id"]),
            ["lead_motion_id", "statute_paragraph_id"],
        )
        if origin.get("lead_motion_id") or origin.get("statute_paragraph_id"):
            msg = "Amendments cannot be forwarded."
            raise PermissionDenied(msg)

    def calculate_all_origin_ids_and_all_derived_motion_ids(
        self, instance: Dict[str, Any]
    ) -> None:
        instance["all_derived_motion_ids"] = []
        if instance.get("origin_id"):
            origin = self.datastore.get(
                FullQualifiedId(Collection("motion"), instance["origin_id"]),
                ["all_origin_ids"],
            )
            instance["all_origin_ids"] = origin.get("all_origin_ids", [])
            instance["all_origin_ids"].append(instance["origin_id"])
        else:
            instance["all_origin_ids"] = []

        # Update the all_derived_motion_ids of the origins
        action_data = []
        for origin_id in instance["all_origin_ids"]:
            origin = self.datastore.get(
                FullQualifiedId(Collection("motion"), origin_id),
                ["all_derived_motion_ids"],
            )
            action_data.append(
                {
                    "id": origin_id,
                    "all_derived_motion_ids": origin.get("all_derived_motion_ids", [])
                    + [instance["id"]],
                }
            )
        if action_data:
            self.execute_other_action(MotionUpdateAllDerivedMotionIds, action_data)

    def check_state_allow_forwarding(self, instance: Dict[str, Any]) -> None:
        origin = self.datastore.get(
            FullQualifiedId(self.model.collection, instance["origin_id"]), ["state_id"]
        )
        state = self.datastore.get(
            FullQualifiedId(Collection("motion_state"), origin["state_id"]),
            ["allow_motion_forwarding"],
        )
        if not state.get("allow_motion_forwarding"):
            raise ActionException("State doesn't allow to forward motion.")
