from ...models.models import Committee
from ..default_schema import DefaultSchema
from ..generics import UpdateAction
from ..register import register_action


@register_action("committee.update")
class CommitteeUpdateAction(UpdateAction):
    """
    Action to update a committee.
    """

    model = Committee()
    schema = DefaultSchema(Committee()).get_update_schema(
        optional_properties=[
            "name",
            "description",
            "template_meeting_id",
            "default_meeting_id",
            "member_ids",
            "manager_ids",
            "forward_to_committee_ids",
        ]
    )
