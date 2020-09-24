from ..base import DummyAction
from ..register import register_action
from . import create  # noqa


@register_action("committee.update")
class CommitteeUpdate(DummyAction):
    pass


@register_action("committee.delete")
class CommitteeDelete(DummyAction):
    pass
