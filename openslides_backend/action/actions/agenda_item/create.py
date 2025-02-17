from typing import Any, Dict

from ....models.models import AgendaItem
from ....permissions.permissions import Permissions
from ....shared.patterns import Collection, FullQualifiedId
from ...mixins.create_action_with_inferred_meeting import (
    CreateActionWithInferredMeeting,
)
from ...util.default_schema import DefaultSchema
from ...util.register import register_action
from ...util.typing import ActionData


@register_action("agenda_item.create")
class AgendaItemCreate(CreateActionWithInferredMeeting):
    """
    Action to create agenda items.
    """

    model = AgendaItem()
    schema = DefaultSchema(AgendaItem()).get_create_schema(
        required_properties=["content_object_id"],
        optional_properties=[
            "item_number",
            "comment",
            "type",
            "parent_id",
            "duration",
            "weight",
        ],
    )
    permission = Permissions.AgendaItem.CAN_MANAGE

    relation_field_for_meeting = "content_object_id"

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        If parent_id is given, set weight to parent.weight + 1
        """
        instance = super().update_instance(instance)
        if instance.get("parent_id") is None:
            return instance
        parent = self.datastore.get(
            FullQualifiedId(Collection("agenda_item"), instance["parent_id"]),
            ["child_ids"],
        )
        max_weight = 0
        for child_id in parent.get("child_ids", []):
            child = self.datastore.get(
                FullQualifiedId(Collection("agenda_item"), child_id),
                ["weight"],
            )
            if child.get("weight", 0) > max_weight:
                max_weight = child["weight"]
        instance["weight"] = max_weight + 1
        return instance

    def get_updated_instances(self, action_data: ActionData) -> ActionData:
        for instance in action_data:
            if instance.get("parent_id") is None:
                parent = {"is_hidden": False, "is_internal": False}
                instance["level"] = 0
            else:
                parent = self.datastore.get(
                    FullQualifiedId(self.model.collection, instance["parent_id"]),
                    ["is_hidden", "is_internal", "level"],
                )
                instance["level"] = parent.get("level", 0) + 1
            instance["is_hidden"] = instance.get(
                "type"
            ) == AgendaItem.HIDDEN_ITEM or parent.get("is_hidden", False)
            instance["is_internal"] = instance.get(
                "type"
            ) == AgendaItem.INTERNAL_ITEM or parent.get("is_internal", False)

        return action_data
