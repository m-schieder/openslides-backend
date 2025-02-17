import time
from typing import Any, Dict

from ....models.models import Motion
from ....permissions.permissions import Permissions
from ....shared.exceptions import ActionException
from ....shared.patterns import Collection, FullQualifiedId
from ...generics.update import UpdateAction
from ...util.default_schema import DefaultSchema
from ...util.register import register_action
from .set_number_mixin import SetNumberMixin


@register_action("motion.reset_state")
class MotionResetStateAction(UpdateAction, SetNumberMixin):
    """
    Reset motion state action.
    """

    model = Motion()
    schema = DefaultSchema(Motion()).get_update_schema()
    permission = Permissions.Motion.CAN_MANAGE_METADATA

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set state_id to motion_state.first_state_of_workflow_id.
        """
        motion = self.datastore.get(
            FullQualifiedId(Collection("motion"), instance["id"]),
            [
                "state_id",
                "meeting_id",
                "lead_motion_id",
                "category_id",
                "number",
                "number_value",
            ],
        )
        if not motion.get("state_id"):
            raise ActionException(f"Motion {instance['id']} has no state.")

        old_state = self.datastore.get(
            FullQualifiedId(Collection("motion_state"), motion["state_id"]),
            ["workflow_id"],
        )
        if not old_state.get("workflow_id"):
            raise ActionException(f"State {motion['state_id']} has no workflow.")

        workflow = self.datastore.get(
            FullQualifiedId(Collection("motion_workflow"), old_state["workflow_id"]),
            ["first_state_id"],
        )
        if not workflow.get("first_state_id"):
            raise ActionException(
                f"State {old_state['workflow_id']} has no first_state_id."
            )
        instance["state_id"] = workflow.get("first_state_id")
        self.set_number(
            instance,
            motion["meeting_id"],
            instance["state_id"],
            motion.get("lead_motion_id"),
            motion.get("category_id"),
            motion.get("number"),
            motion.get("number_value"),
        )
        timestamp = round(time.time())
        instance["last_modified"] = timestamp
        state = self.datastore.get(
            FullQualifiedId(Collection("motion_state"), instance["state_id"]),
            ["set_created_timestamp"],
        )
        instance["created"] = None
        if state.get("set_created_timestamp"):
            instance["created"] = timestamp
        return instance
