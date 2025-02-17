import time
from typing import Any, Dict, List

from ....models.checker import Checker, CheckException
from ....models.models import Meeting
from ....permissions.management_levels import CommitteeManagementLevel
from ....permissions.permission_helper import has_committee_management_level
from ....shared.exceptions import ActionException, PermissionDenied
from ....shared.interfaces.event import EventType
from ....shared.interfaces.write_request import WriteRequest
from ....shared.patterns import KEYSEPARATOR, Collection, FullQualifiedId
from ....shared.schema import id_list_schema
from ...util.default_schema import DefaultSchema
from ...util.register import register_action
from .export_helper import export_meeting
from .import_ import MeetingImport

updatable_fields = [
    "committee_id",
    "welcome_title",
    "description",
    "start_time",
    "end_time",
    "location",
    "organization_tag_ids",
    "name",
]


@register_action("meeting.clone")
class MeetingClone(MeetingImport):
    """
    Action to clone a meeting.
    """

    schema = DefaultSchema(Meeting()).get_default_schema(
        optional_properties=updatable_fields,
        additional_required_fields={"meeting_id": {"type": "integer"}},
        additional_optional_fields={
            "user_ids": id_list_schema,
            "admin_ids": id_list_schema,
        },
    )

    def preprocess_data(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Temporarely, because meeting.clone has _model and _collection attributes
        """
        underscore_keys = tuple(key for key in instance.keys() if key[0] == "_")
        [instance.pop(key) for key in underscore_keys]
        return instance

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        meeting_json = export_meeting(self.datastore, instance["meeting_id"])
        instance["meeting"] = meeting_json
        additional_user_ids = instance.pop("user_ids", None)
        additional_admin_ids = instance.pop("admin_ids", None)

        # checks if the meeting is correct
        self.check_one_meeting(instance)

        if (
            committee_id := instance.get("committee_id")
        ) and committee_id != self.get_meeting_from_json(meeting_json)["committee_id"]:
            self.get_meeting_from_json(meeting_json)["committee_id"] = committee_id

        # pre update the meeting
        name_set = False
        for field in updatable_fields:
            if field in instance:
                if field == "name":
                    name_set = True
                value = instance.pop(field)
                self.get_meeting_from_json(meeting_json)[field] = value
        if not name_set:
            meeting = self.get_meeting_from_json(instance["meeting"])
            meeting["name"] = meeting.get("name", "") + " - Copy"

        # reset mediafile/attachment_ids to [] if None.
        for mediafile_id in instance["meeting"].get("mediafile", []):
            if (
                instance["meeting"]["mediafile"][mediafile_id].get("attachment_ids")
                is None
            ):
                instance["meeting"]["mediafile"][mediafile_id]["attachment_ids"] = []

        # check datavalidation
        checker = Checker(
            data=meeting_json,
            mode="internal",
            repair=True,
            fields_to_remove={
                "motion": [
                    "origin_id",
                    "derived_motion_ids",
                    "all_origin_id",
                    "all_derived_motion_ids",
                ]
            },
        )
        try:
            checker.run_check()
        except CheckException as ce:
            raise ActionException(str(ce))
        self.allowed_collections = checker.allowed_collections

        # set active
        self.get_meeting_from_json(meeting_json)["is_active_in_organization_id"] = 1

        # check limit of meetings
        self.check_limit_of_meetings(
            text="clone",
            text2="",
        )

        # set imported_at
        self.get_meeting_from_json(meeting_json)["imported_at"] = round(time.time())

        # replace ids in the meeting_json
        self.create_replace_map(meeting_json)
        self.duplicate_mediafiles(meeting_json)
        self.replace_fields(instance)

        if additional_user_ids:
            default_group_id = self.get_meeting_from_json(instance["meeting"]).get(
                "default_group_id"
            )
            self._update_default_and_admin_group(
                default_group_id, instance, additional_user_ids
            )

        if additional_admin_ids:
            admin_group_id = self.get_meeting_from_json(instance["meeting"]).get(
                "admin_group_id"
            )
            self._update_default_and_admin_group(
                admin_group_id, instance, additional_admin_ids
            )
        return instance

    @staticmethod
    def _update_default_and_admin_group(
        group_id: int, instance: Dict[str, Any], additional_user_ids: List[int]
    ) -> None:
        for entry in instance["meeting"].get("group", {}).values():
            if entry["id"] == group_id:
                user_ids = set(entry.get("user_ids", set()) or set())
                user_ids.update(additional_user_ids)
                entry["user_ids"] = list(user_ids)

    def duplicate_mediafiles(self, json_data: Dict[str, Any]) -> None:
        for mediafile_id in json_data["mediafile"]:
            mediafile = json_data["mediafile"][mediafile_id]
            if not mediafile.get("is_directory"):
                self.media.duplicate_mediafile(
                    mediafile["id"], self.replace_map["mediafile"][mediafile["id"]]
                )

    def append_extra_write_requests(
        self, write_requests: List[WriteRequest], json_data: Dict[str, Any]
    ) -> None:

        updated_field_n_n = (
            (
                "group",
                "user_ids",
                "group_$_ids",
            ),
            (
                "motion",
                "supporter_ids",
                "supported_motion_$_ids",
            ),
            (
                "poll",
                "voted_ids",
                "poll_voted_$_ids",
            ),
        )
        for tuple_ in updated_field_n_n:
            self.append_helper_list_list(write_requests, json_data, *tuple_)

        updated_field_n_1 = (
            (
                "speaker",
                "user_id",
                "speaker_$_ids",
            ),
            (
                "personal_note",
                "user_id",
                "personal_note_$_ids",
            ),
            (
                "motion_submitter",
                "user_id",
                "submitted_motion_$_ids",
            ),
            (
                "vote",
                "user_id",
                "vote_$_ids",
            ),
            (
                "vote",
                "delegated_user_id",
                "vote_delegated_vote_$_ids",
            ),
            (
                "assignment_candidate",
                "user_id",
                "assignment_candidate_$_ids",
            ),
        )
        for tuple_ in updated_field_n_1:
            self.append_helper_list_int(write_requests, json_data, *tuple_)

        updated_field_n_co = (
            (
                "option",
                "content_object_id",
                "option_$_ids",
            ),
            (
                "projection",
                "content_object_id",
                "projection_$_ids",
            ),
        )
        for tuple_ in updated_field_n_co:
            self.append_helper_list_cobj(write_requests, json_data, *tuple_)

    def field_with_meeting(self, field: str, json_data: Dict[str, Any]) -> str:
        front, back = field.split("$")
        return f"{front}${self.get_meeting_from_json(json_data)['id']}{back}"

    def append_helper_list_int(
        self,
        write_requests: List[WriteRequest],
        json_data: Dict[str, Any],
        collection: str,
        field: str,
        field_template: str,
    ) -> None:
        for model in json_data[collection].values():
            if model.get(field):
                write_requests.append(
                    self.build_write_request_helper(
                        model[field], json_data, field_template, model["id"]
                    )
                )

    def append_helper_list_list(
        self,
        write_requests: List[WriteRequest],
        json_data: Dict[str, Any],
        collection: str,
        field: str,
        field_template: str,
    ) -> None:
        for model in json_data[collection].values():
            if model.get(field):
                for user_id in model.get(field):
                    write_requests.append(
                        self.build_write_request_helper(
                            user_id, json_data, field_template, model["id"]
                        )
                    )

    def append_helper_list_cobj(
        self,
        write_requests: List[WriteRequest],
        json_data: Dict[str, Any],
        collection: str,
        field: str,
        field_template: str,
    ) -> None:
        for model in json_data[collection].values():
            if model.get(field):
                fqid = model[field]
                cobj_collection, cobj_id = fqid.split(KEYSEPARATOR)
                if cobj_collection == "user":
                    write_requests.append(
                        self.build_write_request_helper(
                            cobj_id, json_data, field_template, model["id"]
                        )
                    )

    def build_write_request_helper(
        self,
        user_id: int,
        json_data: Dict[str, Any],
        field_template: str,
        model_id: int,
    ) -> WriteRequest:
        return self.build_write_request(
            EventType.Update,
            FullQualifiedId(Collection("user"), user_id),
            f"clone meeting {self.get_meeting_from_json(json_data)['id']}",
            list_fields={
                "add": {
                    field_template: [str(self.get_meeting_from_json(json_data)["id"])],
                    self.field_with_meeting(field_template, json_data): [model_id],
                },
                "remove": {},
            },
        )

    def check_permissions(self, instance: Dict[str, Any]) -> None:
        if instance.get("committee_id"):
            committee_id = instance["committee_id"]
        else:
            meeting = self.datastore.get(
                FullQualifiedId(Collection("meeting"), instance["meeting_id"]),
                ["committee_id"],
            )
            committee_id = meeting["committee_id"]
        if not has_committee_management_level(
            self.datastore,
            self.user_id,
            CommitteeManagementLevel.CAN_MANAGE,
            committee_id,
        ):
            raise PermissionDenied(
                f"Missing {CommitteeManagementLevel.CAN_MANAGE.get_verbose_type()}: {CommitteeManagementLevel.CAN_MANAGE} for committee {committee_id}"
            )
