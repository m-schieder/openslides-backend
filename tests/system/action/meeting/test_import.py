import base64
import time
from typing import Any, Dict, List, cast

from migrations import get_backend_migration_index
from openslides_backend.models.models import Meeting
from tests.system.action.base import BaseActionTestCase

current_migration_index = get_backend_migration_index()


class MeetingImport(BaseActionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.set_models(
            {
                "organization/1": {"active_meeting_ids": [1], "committee_ids": [1]},
                "committee/1": {"organization_id": 1, "meeting_ids": [1]},
                "meeting/1": {"committee_id": 1, "group_ids": [1]},
                "group/1": {"meeting_id": 1},
                "projector/1": {"meeting_id": 1},
                "motion/1": {
                    "meeting_id": 1,
                    "sequential_number": 26,
                    "number_value": 31,
                },
            }
        )

    def create_request_data(self, datapart: Dict[str, Any]) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "committee_id": 1,
            "meeting": {
                "_migration_index": current_migration_index,
                "meeting": {
                    "1": {
                        "id": 1,
                        "name": "Test",
                        "description": "blablabla",
                        "admin_group_id": 1,
                        "default_group_id": 1,
                        "motions_default_amendment_workflow_id": 1,
                        "motions_default_statute_amendment_workflow_id": 1,
                        "motions_default_workflow_id": 1,
                        "projector_countdown_default_time": 60,
                        "projector_countdown_warning_time": 60,
                        "reference_projector_id": 1,
                        "user_ids": [1],
                        "imported_at": None,
                        "custom_translations": None,
                        "template_for_organization_id": None,
                        "enable_anonymous": False,
                        "location": "",
                        "start_time": 10,
                        "end_time": 10,
                        "welcome_title": "Welcome to OpenSlides",
                        "welcome_text": "[Space for your welcome text.]",
                        "conference_show": False,
                        "conference_auto_connect": False,
                        "conference_los_restriction": False,
                        "conference_stream_url": "",
                        "conference_stream_poster_url": "",
                        "conference_open_microphone": True,
                        "conference_open_video": True,
                        "conference_auto_connect_next_speakers": 1,
                        "conference_enable_helpdesk": False,
                        "applause_enable": True,
                        "applause_type": "applause-type-particles",
                        "applause_show_level": True,
                        "applause_min_amount": 2,
                        "applause_max_amount": 3,
                        "applause_timeout": 6,
                        "applause_particle_image_url": "test",
                        "export_csv_encoding": "utf-8",
                        "export_csv_separator": ",",
                        "export_pdf_pagenumber_alignment": "center",
                        "export_pdf_fontsize": 10,
                        "export_pdf_pagesize": "A4",
                        "export_pdf_line_height": 1.25,
                        "export_pdf_page_margin_left": 20,
                        "export_pdf_page_margin_top": 25,
                        "export_pdf_page_margin_right": 20,
                        "export_pdf_page_margin_bottom": 20,
                        "agenda_show_subtitles": False,
                        "agenda_enable_numbering": True,
                        "agenda_number_prefix": "",
                        "agenda_numeral_system": "arabic",
                        "agenda_item_creation": "default_yes",
                        "agenda_new_items_default_visibility": "internal",
                        "agenda_show_internal_items_on_projector": False,
                        "list_of_speakers_amount_last_on_projector": 1,
                        "list_of_speakers_amount_next_on_projector": 1,
                        "list_of_speakers_couple_countdown": True,
                        "list_of_speakers_show_amount_of_speakers_on_slide": True,
                        "list_of_speakers_present_users_only": False,
                        "list_of_speakers_show_first_contribution": False,
                        "list_of_speakers_enable_point_of_order_speakers": True,
                        "list_of_speakers_enable_pro_contra_speech": True,
                        "list_of_speakers_can_set_contribution_self": True,
                        "list_of_speakers_speaker_note_for_everyone": True,
                        "list_of_speakers_initially_closed": True,
                        "motions_preamble": "The assembly may decide:",
                        "motions_default_line_numbering": "none",
                        "motions_line_length": 90,
                        "motions_reason_required": False,
                        "motions_enable_text_on_projector": True,
                        "motions_enable_reason_on_projector": True,
                        "motions_enable_sidebox_on_projector": True,
                        "motions_enable_recommendation_on_projector": True,
                        "motions_show_referring_motions": True,
                        "motions_show_sequential_number": True,
                        "motions_recommendations_by": "ABK",
                        "motions_statute_recommendations_by": "Statute ABK",
                        "motions_recommendation_text_mode": "original",
                        "motions_default_sorting": "number",
                        "motions_number_type": "per_category",
                        "motions_number_min_digits": 3,
                        "motions_number_with_blank": False,
                        "motions_statutes_enabled": True,
                        "motions_amendments_enabled": True,
                        "motions_amendments_in_main_list": True,
                        "motions_amendments_of_amendments": True,
                        "motions_amendments_prefix": "Ä-",
                        "motions_amendments_text_mode": "freestyle",
                        "motions_amendments_multiple_paragraphs": True,
                        "motions_supporters_min_amount": 1,
                        "motions_export_title": "Motions",
                        "motions_export_preamble": "an export preamble",
                        "motions_export_submitter_recommendation": True,
                        "motions_export_follow_recommendation": True,
                        "motion_poll_ballot_paper_selection": "CUSTOM_NUMBER",
                        "motion_poll_ballot_paper_number": 8,
                        "motion_poll_default_type": "pseudoanonymous",
                        "motion_poll_default_100_percent_base": "YNA",
                        "motion_poll_default_group_ids": [],
                        "motion_poll_default_backend": "fast",
                        "users_sort_by": "first_name",
                        "users_enable_presence_view": True,
                        "users_enable_vote_weight": True,
                        "users_allow_self_set_present": True,
                        "users_pdf_welcometitle": "Welcome to OpenSlides",
                        "users_pdf_welcometext": "[Place for your welcome and help text.]",
                        "users_pdf_wlan_ssid": "",
                        "users_pdf_wlan_password": "",
                        "users_pdf_wlan_encryption": "",
                        "users_email_sender": "noreply@yourdomain.com",
                        "users_email_replyto": "",
                        "users_email_subject": "OpenSlides access data",
                        "users_email_body": "Dear {name},\n\nthis is your personal OpenSlides login:\n\n{url}\nUsername: {username}\nPassword: {password}\n\n\nThis email was generated automatically.",
                        "assignments_export_title": "Elections",
                        "assignments_export_preamble": "",
                        "assignment_poll_ballot_paper_selection": "CUSTOM_NUMBER",
                        "assignment_poll_ballot_paper_number": 8,
                        "assignment_poll_add_candidates_to_list_of_speakers": True,
                        "assignment_poll_enable_max_votes_per_option": None,
                        "assignment_poll_sort_poll_result_by_votes": True,
                        "assignment_poll_default_type": "pseudoanonymous",
                        "assignment_poll_default_method": "votes",
                        "assignment_poll_default_100_percent_base": "valid",
                        "assignment_poll_default_group_ids": [],
                        "assignment_poll_default_backend": "fast",
                        "poll_ballot_paper_selection": "CUSTOM_NUMBER",
                        "poll_ballot_paper_number": 8,
                        "poll_sort_poll_result_by_votes": True,
                        "poll_default_type": "pseudoanonymous",
                        "poll_default_method": "votes",
                        "poll_default_100_percent_base": "valid",
                        "poll_default_group_ids": [],
                        "poll_default_backend": "fast",
                        "poll_couple_countdown": True,
                        "projector_ids": [1],
                        "all_projection_ids": [],
                        "projector_message_ids": [],
                        "projector_countdown_ids": [],
                        "tag_ids": [],
                        "agenda_item_ids": [],
                        "list_of_speakers_ids": [],
                        "speaker_ids": [],
                        "topic_ids": [],
                        "group_ids": [1],
                        "mediafile_ids": [],
                        "motion_ids": [],
                        "motion_submitter_ids": [],
                        "motion_comment_section_ids": [],
                        "motion_comment_ids": [],
                        "motion_state_ids": [1],
                        "motion_category_ids": [],
                        "motion_block_ids": [],
                        "motion_workflow_ids": [1],
                        "motion_statute_paragraph_ids": [],
                        "motion_change_recommendation_ids": [],
                        "poll_ids": [],
                        "option_ids": [],
                        "vote_ids": [],
                        "assignment_ids": [],
                        "assignment_candidate_ids": [],
                        "personal_note_ids": [],
                        "chat_group_ids": [],
                        "chat_message_ids": [],
                        "logo_$_id": [],
                        "font_$_id": [],
                        "committee_id": None,
                        "is_active_in_organization_id": None,
                        "is_archived_in_organization_id": None,
                        "default_meeting_for_committee_id": None,
                        "organization_tag_ids": [],
                        "present_user_ids": [],
                        "list_of_speakers_countdown_id": None,
                        "poll_countdown_id": None,
                        "default_projector_$_id": Meeting.default_projector__id.replacement_enum,
                        **{
                            f"default_projector_${name}_id": 1
                            for name in cast(
                                List[str],
                                Meeting.default_projector__id.replacement_enum,
                            )
                        },
                        "projection_ids": [],
                    }
                },
                "user": {
                    "1": self.get_user_data(
                        1,
                        {
                            "group_$_ids": ["1"],
                            "group_$1_ids": [1],
                            "is_active": True,
                        },
                    ),
                },
                "group": {
                    "1": self.get_group_data(
                        1,
                        {
                            "user_ids": [1],
                            "admin_group_for_meeting_id": 1,
                            "default_group_for_meeting_id": 1,
                        },
                    )
                },
                "motion_workflow": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "name": "blup",
                        "first_state_id": 1,
                        "default_amendment_workflow_meeting_id": 1,
                        "default_statute_amendment_workflow_meeting_id": 1,
                        "default_workflow_meeting_id": 1,
                        "state_ids": [1],
                        "sequential_number": 1,
                    }
                },
                "motion_state": {
                    "1": {
                        "id": 1,
                        "css_class": "lightblue",
                        "meeting_id": 1,
                        "workflow_id": 1,
                        "name": "test",
                        "weight": 1,
                        "recommendation_label": None,
                        "restrictions": [],
                        "allow_support": True,
                        "allow_create_poll": True,
                        "allow_submitter_edit": True,
                        "set_number": True,
                        "show_state_extension_field": False,
                        "merge_amendment_into_final": "undefined",
                        "show_recommendation_extension_field": False,
                        "next_state_ids": [],
                        "previous_state_ids": [],
                        "motion_ids": [],
                        "motion_recommendation_ids": [],
                        "workflow_id": 1,
                        "first_state_of_workflow_id": 1,
                    }
                },
                "projector": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "used_as_reference_projector_meeting_id": 1,
                        "name": "Default projector",
                        "scale": 10,
                        "scroll": 10,
                        "width": 1220,
                        "aspect_ratio_numerator": 4,
                        "aspect_ratio_denominator": 3,
                        "color": "#000000",
                        "background_color": "#ffffff",
                        "header_background_color": "#317796",
                        "header_font_color": "#f5f5f5",
                        "header_h1_color": "#317796",
                        "chyron_background_color": "#317796",
                        "chyron_font_color": "#ffffff",
                        "show_header_footer": True,
                        "show_title": True,
                        "show_logo": True,
                        "show_clock": True,
                        "current_projection_ids": [],
                        "preview_projection_ids": [],
                        "history_projection_ids": [],
                        "used_as_default_$_in_meeting_id": Meeting.default_projector__id.replacement_enum,
                        **{
                            f"used_as_default_${name}_in_meeting_id": 1
                            for name in cast(
                                List[str],
                                Meeting.default_projector__id.replacement_enum,
                            )
                        },
                        "sequential_number": 1,
                    }
                },
            },
        }
        for collection, models in datapart.items():
            if collection not in data["meeting"]:
                data["meeting"][collection] = models
            else:
                data["meeting"][collection].update(models)

        needed_collections = (
            "user",
            "meeting",
            "group",
            "personal_note",
            "tag",
            "agenda_item",
            "list_of_speakers",
            "speaker",
            "topic",
            "motion",
            "motion_submitter",
            "motion_comment",
            "motion_comment_section",
            "motion_category",
            "motion_block",
            "motion_change_recommendation",
            "motion_state",
            "motion_workflow",
            "motion_statute_paragraph",
            "poll",
            "option",
            "vote",
            "assignment",
            "assignment_candidate",
            "mediafile",
            "projector",
            "projection",
            "projector_message",
            "projector_countdown",
            "chat_group",
            "chat_message",
        )
        for collection in needed_collections:
            if collection not in data["meeting"].keys():
                data["meeting"][collection] = {}

        return data

    def get_user_data(self, obj_id: int, data: Dict[str, Any] = {}) -> Dict[str, Any]:
        return {
            "id": obj_id,
            "password": "",
            "username": "test",
            "group_$_ids": [],
            "committee_ids": [],
            "committee_$_management_level": [],
            "vote_weight_$": [],
            "title": "",
            "pronoun": "",
            "first_name": "",
            "last_name": "Administrator",
            "is_active": True,
            "is_physical_person": True,
            "default_password": "admin",
            "can_change_own_password": True,
            "gender": "male",
            "email": "",
            "default_number": "",
            "default_structure_level": "",
            "default_vote_weight": "1.000000",
            "last_email_send": None,
            "is_demo_user": False,
            "organization_management_level": None,
            "is_present_in_meeting_ids": [],
            "comment_$": [],
            "number_$": [],
            "structure_level_$": [],
            "about_me_$": [],
            "speaker_$_ids": [],
            "personal_note_$_ids": [],
            "supported_motion_$_ids": [],
            "submitted_motion_$_ids": [],
            "assignment_candidate_$_ids": [],
            "poll_voted_$_ids": [],
            "option_$_ids": [],
            "vote_$_ids": [],
            "projection_$_ids": [],
            "vote_delegated_vote_$_ids": [],
            "vote_delegated_$_to_id": [],
            "vote_delegations_$_from_ids": [],
            "chat_message_$_ids": [],
            "meeting_ids": [1],
            **data,
        }

    def get_group_data(self, obj_id: int, data: Dict[str, Any] = {}) -> Dict[str, Any]:
        return {
            "id": obj_id,
            "meeting_id": 1,
            "name": "testgroup",
            "weight": obj_id,
            "user_ids": [],
            "admin_group_for_meeting_id": None,
            "default_group_for_meeting_id": None,
            "permissions": [],
            "mediafile_access_group_ids": [],
            "mediafile_inherited_access_group_ids": [],
            "read_comment_section_ids": [],
            "write_comment_section_ids": [],
            "read_chat_group_ids": [],
            "write_chat_group_ids": [],
            "poll_ids": [],
            "used_as_motion_poll_default_id": None,
            "used_as_assignment_poll_default_id": None,
            "used_as_poll_default_id": None,
            **data,
        }

    def get_motion_data(self, obj_id: int, data: Dict[str, Any] = {}) -> Dict[str, Any]:
        return {
            "id": obj_id,
            "meeting_id": 1,
            "list_of_speakers_id": 1,
            "state_id": 1,
            "title": "bla",
            "number": "1 - 1",
            "number_value": 1,
            "sequential_number": 2,
            "text": "<p>l&ouml;mk</p>",
            "amendment_paragraph_$": [],
            "modified_final_version": "",
            "reason": "",
            "category_weight": 10000,
            "state_extension": "<p>regeer</p>",
            "recommendation_extension": None,
            "sort_weight": 10000,
            "created": 1584512346,
            "last_modified": 1584512346,
            "start_line_number": 1,
            **data,
        }

    def get_mediafile_data(
        self, obj_id: int, data: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        file_content = base64.b64encode(b"testtesttest").decode()
        return {
            "id": obj_id,
            "owner_id": "meeting/1",
            "blob": file_content,
            "title": "A.txt",
            "is_directory": False,
            "filesize": 3,
            "filename": "A.txt",
            "mimetype": "text/plain",
            "pdf_information": {},
            "create_timestamp": 1584513771,
            "is_public": True,
            "access_group_ids": [],
            "inherited_access_group_ids": [],
            "parent_id": None,
            "child_ids": [],
            "list_of_speakers_id": None,
            "projection_ids": [],
            "attachment_ids": [],
            "used_as_logo_$_in_meeting_id": [],
            "used_as_font_$_in_meeting_id": [],
            **data,
        }

    def test_no_meeting_collection(self) -> None:
        response = self.request(
            "meeting.import",
            {
                "committee_id": 1,
                "meeting": {
                    "meeting": {},
                    "_migration_index": current_migration_index,
                },
            },
        )
        self.assert_status_code(response, 400)
        assert (
            "Need exactly one meeting in meeting collection."
            in response.json["message"]
        )

    def test_too_many_meeting_collections(self) -> None:
        response = self.request(
            "meeting.import",
            {
                "committee_id": 1,
                "meeting": {
                    "meeting": {"1": {"id": 1}, "2": {"id": 2}},
                    "_migration_index": current_migration_index,
                },
            },
        )
        self.assert_status_code(response, 400)
        assert (
            "Need exactly one meeting in meeting collection."
            in response.json["message"]
        )

    def test_include_organization(self) -> None:
        request_data = self.create_request_data({"organization": {"1": {"id": 1}}})

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert "Invalid collections: organization." in response.json["message"]

    def test_replace_ids_and_write_to_datastore(self) -> None:
        request_data = self.create_request_data(
            {
                "personal_note": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "note": "<p>Some content..</p>",
                        "star": False,
                        "user_id": 1,
                    }
                },
                "motion": {
                    "1": self.get_motion_data(
                        1,
                        {
                            "tag_ids": [1],
                            "personal_note_ids": [1],
                        },
                    )
                },
                "list_of_speakers": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "closed": False,
                        "sequential_number": 1,
                        "speaker_ids": [],
                        "projection_ids": [],
                    }
                },
                "tag": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "tagged_ids": ["motion/1"],
                        "name": "testag",
                    }
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["personal_note_ids"] = [1]
        request_data["meeting"]["user"]["1"]["personal_note_$_ids"] = ["1"]
        request_data["meeting"]["user"]["1"]["personal_note_$1_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["list_of_speakers_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["tag_ids"] = [1]

        start = round(time.time())
        response = self.request("meeting.import", request_data)
        end = round(time.time()) + 1
        self.assert_status_code(response, 200)
        meeting_2 = self.assert_model_exists(
            "meeting/2",
            {
                "name": "Test",
                "description": "blablabla",
                "committee_id": 1,
                "enable_anonymous": False,
                "is_active_in_organization_id": 1,
            },
        )
        assert start <= meeting_2.get("imported_at", 0) <= end
        user_2 = self.assert_model_exists(
            "user/2", {"username": "test", "group_$2_ids": [2], "group_$_ids": ["2"]}
        )
        assert user_2.get("password", "")
        self.assert_model_exists("projector/2", {"meeting_id": 2})
        self.assert_model_exists("group/2", {"user_ids": [1, 2]})
        self.assert_model_exists(
            "personal_note/1",
            {"content_object_id": "motion/2", "user_id": 2, "meeting_id": 2},
        )
        self.assert_model_exists(
            "tag/1", {"tagged_ids": ["motion/2"], "name": "testag"}
        )
        committee_1 = self.get_model("committee/1")
        self.assertCountEqual(committee_1.get("meeting_ids"), [1, 2])
        self.assertCountEqual(committee_1.get("user_ids"), [1, 2])
        self.assert_model_exists("organization/1", {"active_meeting_ids": [1, 2]})

    def test_check_calc_fields(self) -> None:
        request_data = self.create_request_data({})
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists("user/2", {"meeting_ids": [2]})
        meeting2 = self.assert_model_exists("meeting/2")
        self.assertCountEqual(meeting2["user_ids"], [1, 2])

    def test_check_usernames_1(self) -> None:
        self.set_models(
            {
                "user/1": {"username": "admin"},
            }
        )
        request_data = self.create_request_data(
            {
                "user": {
                    "1": self.get_user_data(
                        1,
                        {
                            "username": "admin",
                            "group_$_ids": ["1"],
                            "group_$1_ids": [1],
                        },
                    ),
                },
            }
        )
        self.assert_model_exists("user/1", {"username": "admin"})

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)

        organization = self.assert_model_exists("organization/1")
        self.assertCountEqual(organization["active_meeting_ids"], [1, 2])

        committee1 = self.assert_model_exists(
            "committee/1",
        )
        self.assertCountEqual(committee1["user_ids"], [1, 2])
        self.assertCountEqual(committee1["meeting_ids"], [1, 2])

        imported_meeting = self.assert_model_exists(
            "meeting/2",
            {
                "group_ids": [2],
                "committee_id": 1,
                "projector_ids": [2],
                "admin_group_id": 2,
                "default_group_id": 2,
                "motion_state_ids": [1],
                "motion_workflow_ids": [1],
                "is_active_in_organization_id": 1,
            },
        )
        self.assertCountEqual(imported_meeting["user_ids"], [1, 2])

        self.assert_model_exists(
            "user/1",
            {
                "username": "admin",
                "group_$_ids": ["2"],
                "group_$2_ids": [2],
                "meeting_ids": [2],
            },
        )
        self.assert_model_exists(
            "user/2",
            {
                "username": "admin1",
                "group_$_ids": ["2"],
                "group_$2_ids": [2],
                "meeting_ids": [2],
                "committee_ids": [1],
            },
        )
        self.assert_model_exists(
            "group/2",
            {
                "user_ids": [1, 2],
                "meeting_id": 2,
                "admin_group_for_meeting_id": 2,
                "default_group_for_meeting_id": 2,
            },
        )

    def test_check_usernames_2(self) -> None:
        self.set_models(
            {
                "user/1": {"username": "admin"},
            }
        )
        request_data = self.create_request_data({})
        request_data["meeting"]["user"]["1"] = self.get_user_data(
            1,
            {
                "username": "admin",
                "group_$_ids": ["1"],
                "group_$1_ids": [1],
            },
        )
        request_data["meeting"]["user"]["2"] = self.get_user_data(
            2,
            {
                "username": "admin1",
            },
        )

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "user/1",
            {
                "username": "admin",
                "group_$_ids": ["2"],
                "group_$2_ids": [2],
                "meeting_ids": [2],
            },
        )
        self.assert_model_exists("user/2", {"username": "admin1"})
        self.assert_model_exists("user/3", {"username": "admin11"})
        self.assert_model_exists("group/2", {"user_ids": [1, 2], "meeting_id": 2})

    def test_check_negative_default_vote_weight(self) -> None:
        request_data = self.create_request_data({})
        request_data["meeting"]["user"]["1"] = self.get_user_data(
            1,
            {
                "default_vote_weight": "-1.123456",
                "group_$_ids": ["1"],
                "group_$1_ids": [1],
            },
        )

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        self.assertIn(
            "default_vote_weight must be bigger than or equal to 0.",
            response.json["message"],
        )

    def test_double_import(self) -> None:
        start = round(time.time())
        self.set_models(
            {
                "user/1": {"username": "admin"},
            }
        )
        request_data = self.create_request_data(
            {
                "personal_note": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "note": "<p>Some content..</p>",
                        "star": False,
                        "user_id": 1,
                    }
                },
                "motion": {
                    "1": self.get_motion_data(
                        1,
                        {
                            "tag_ids": [1],
                            "personal_note_ids": [1],
                        },
                    )
                },
                "list_of_speakers": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "closed": False,
                        "sequential_number": 1,
                        "speaker_ids": [],
                        "projection_ids": [],
                    }
                },
                "tag": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "tagged_ids": ["motion/1"],
                        "name": "testag",
                    }
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["personal_note_ids"] = [1]
        request_data["meeting"]["user"]["1"]["personal_note_$_ids"] = ["1"]
        request_data["meeting"]["user"]["1"]["personal_note_$1_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["list_of_speakers_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["tag_ids"] = [1]

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists("user/2", {"username": "test"})
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "user/3", {"username": "test1", "group_$3_ids": [3], "group_$_ids": ["3"]}
        )
        meeting_3 = self.assert_model_exists(
            "meeting/3",
            {
                "name": "Test",
                "description": "blablabla",
                "committee_id": 1,
                "enable_anonymous": False,
            },
        )
        assert start <= meeting_3.get("imported_at", 0) <= start + 300
        self.assert_model_exists("projector/3", {"meeting_id": 3})
        self.assert_model_exists("group/3", {"user_ids": [1, 3]})
        self.assert_model_exists(
            "personal_note/2", {"content_object_id": "motion/3", "meeting_id": 3}
        )
        self.assert_model_exists(
            "tag/2", {"tagged_ids": ["motion/3"], "name": "testag", "meeting_id": 3}
        )
        committee_1 = self.get_model("committee/1")
        self.assertCountEqual(committee_1.get("user_ids"), [1, 2, 3])
        self.assertCountEqual(committee_1.get("meeting_ids"), [1, 2, 3])

    def test_no_permission(self) -> None:
        self.set_models(
            {
                "user/1": {
                    "username": "admin",
                    "organization_management_level": "can_manage_users",
                },
            }
        )
        response = self.request("meeting.import", self.create_request_data({}))
        self.assert_status_code(response, 403)
        assert (
            "Missing CommitteeManagementLevel: can_manage" in response.json["message"]
        )

    def test_use_blobs(self) -> None:
        file_content = base64.b64encode(b"testtesttest").decode()
        request_data = self.create_request_data(
            {
                "mediafile": {"1": self.get_mediafile_data(1)},
            }
        )
        request_data["meeting"]["meeting"]["1"]["mediafile_ids"] = [1]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        mediafile = self.get_model("mediafile/1")
        assert mediafile.get("blob") is None
        self.media.upload_mediafile.assert_called_with(file_content, 1, "text/plain")

    def test_inherited_access_group_ids_none(self) -> None:
        request_data = self.create_request_data(
            {
                "mediafile": {
                    "1": self.get_mediafile_data(
                        1,
                        {
                            "access_group_ids": None,
                            "inherited_access_group_ids": None,
                        },
                    ),
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["mediafile_ids"] = [1]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)

    def test_inherited_access_group_ids_wrong_order(self) -> None:
        request_data = self.create_request_data(
            {
                "group": {
                    "1": self.get_group_data(
                        1,
                        {
                            "user_ids": [1],
                            "admin_group_for_meeting_id": 1,
                            "default_group_for_meeting_id": 1,
                            "mediafile_access_group_ids": [1],
                            "mediafile_inherited_access_group_ids": [1],
                        },
                    ),
                    "2": self.get_group_data(
                        2,
                        {
                            "mediafile_access_group_ids": [1],
                            "mediafile_inherited_access_group_ids": [1],
                        },
                    ),
                },
                "mediafile": {
                    "1": self.get_mediafile_data(
                        1,
                        {
                            "is_public": False,
                            "access_group_ids": [1, 2],
                            "inherited_access_group_ids": [1, 2],
                        },
                    ),
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["mediafile_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["group_ids"] = [1, 2]
        # try both orders, both should work
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        # other order
        request_data["meeting"]["mediafile"]["1"]["inherited_access_group_ids"] = [2, 1]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)

    def test_meeting_user_ids(self) -> None:
        # Calculated field.
        # User/1 is in user_ids, because calling user is added
        response = self.request("meeting.import", self.create_request_data({}))
        self.assert_status_code(response, 200)
        meeting2 = self.assert_model_exists("meeting/2")
        self.assertCountEqual(meeting2["user_ids"], [1, 2])
        self.assert_model_exists("user/2", {"meeting_ids": [2]})

    def test_motion_recommendation_extension(self) -> None:
        # Special field
        request_data = self.create_request_data(
            {
                "motion": {
                    "1": self.get_motion_data(1),
                    "2": self.get_motion_data(
                        2,
                        {
                            "id": 2,
                            "list_of_speakers_id": 2,
                            "recommendation_extension": "bla[motion/1]bla",
                        },
                    ),
                },
                "list_of_speakers": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "closed": False,
                        "sequential_number": 1,
                        "speaker_ids": [],
                        "projection_ids": [],
                    },
                    "2": {
                        "id": 2,
                        "meeting_id": 1,
                        "content_object_id": "motion/2",
                        "closed": False,
                        "sequential_number": 2,
                        "speaker_ids": [],
                        "projection_ids": [],
                    },
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1, 2]
        request_data["meeting"]["meeting"]["1"]["list_of_speakers_ids"] = [1, 2]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1, 2]

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "motion/3", {"recommendation_extension": "bla[motion/2]bla"}
        )

    def test_motion_recommendation_extension_missing_model(self) -> None:
        # Special field
        request_data = self.create_request_data(
            {
                "motion": {
                    "1": self.get_motion_data(1),
                    "2": self.get_motion_data(
                        2,
                        {
                            "id": 2,
                            "list_of_speakers_id": 2,
                            "recommendation_extension": "bla[motion/11]bla",
                        },
                    ),
                },
                "list_of_speakers": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "closed": False,
                        "speaker_ids": [],
                        "projection_ids": [],
                    },
                    "2": {
                        "id": 2,
                        "meeting_id": 1,
                        "content_object_id": "motion/2",
                        "closed": False,
                        "speaker_ids": [],
                        "projection_ids": [],
                    },
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1, 2]
        request_data["meeting"]["meeting"]["1"]["list_of_speakers_ids"] = [1, 2]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1, 2]

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert (
            "Found motion/11 in recommendation_extension but not in models."
            in response.json["message"]
        )

    def test_logo_dollar_id(self) -> None:
        # Template Relation Field
        request_data = self.create_request_data(
            {
                "mediafile": {
                    "3": self.get_mediafile_data(
                        3,
                        {
                            "used_as_logo_$_in_meeting_id": ["web_header"],
                            "used_as_logo_$web_header_in_meeting_id": 1,
                        },
                    )
                }
            }
        )
        request_data["meeting"]["meeting"]["1"]["logo_$_id"] = ["web_header"]
        request_data["meeting"]["meeting"]["1"]["logo_$web_header_id"] = 3
        request_data["meeting"]["meeting"]["1"]["mediafile_ids"] = [3]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists("mediafile/1")
        self.assert_model_exists(
            "meeting/2", {"logo_$_id": ["web_header"], "logo_$web_header_id": 1}
        )

    def test_is_public_error(self) -> None:
        request_data = self.create_request_data(
            {
                "mediafile": {
                    "3": self.get_mediafile_data(
                        3,
                        {
                            "used_as_logo_$_in_meeting_id": ["web_header"],
                            "used_as_logo_$web_header_in_meeting_id": 1,
                            "parent_id": 2,
                        },
                    ),
                    "2": self.get_mediafile_data(
                        2,
                        {
                            "title": "dir",
                            "is_directory": True,
                            "filesize": 0,
                            "filename": None,
                            "mimetype": None,
                            "is_public": False,
                            "child_ids": [3],
                        },
                    ),
                }
            }
        )
        request_data["meeting"]["meeting"]["1"]["logo_$_id"] = ["web_header"]
        request_data["meeting"]["meeting"]["1"]["logo_$web_header_id"] = 3
        request_data["meeting"]["meeting"]["1"]["mediafile_ids"] = [2, 3]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert "mediafile/3: is_public is wrong." in response.json["message"]

    def test_request_user_in_admin_group(self) -> None:
        response = self.request("meeting.import", self.create_request_data({}))
        self.assert_status_code(response, 200)
        self.assert_model_exists("user/1", {"group_$_ids": ["2"], "group_$2_ids": [2]})
        meeting = self.assert_model_exists("meeting/2")
        self.assertCountEqual(meeting["user_ids"], [1, 2])
        group2 = self.assert_model_exists("group/2")
        self.assertCountEqual(group2["user_ids"], [1, 2])

    def test_motion_all_derived_motion_ids(self) -> None:
        """
        repair and fields_to_remove delete the motion forwarding fields
        (all_)origin_id and (all_)derived_motion_ids. Otherwise the meeting
        couldn't be imported with relations to other meeting.
        """
        request_data = self.create_request_data(
            {
                "motion": {
                    "1": self.get_motion_data(
                        1,
                        {
                            "all_derived_motion_ids": [1],
                            "list_of_speakers_id": 1,
                            "state_id": 1,
                        },
                    ),
                },
                "list_of_speakers": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "closed": False,
                        "sequential_number": 1,
                        "speaker_ids": [],
                        "projection_ids": [],
                    }
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["list_of_speakers_ids"] = [1]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "motion/2",
            {
                "meeting_id": 2,
                "origin_id": None,
                "derived_motion_ids": None,
                "all_origin_id": None,
                "all_derived_motion_ids": None,
            },
        )

    def test_motion_all_origin_ids(self) -> None:
        request_data = self.create_request_data(
            {
                "motion": {
                    "1": self.get_motion_data(
                        1,
                        {
                            "all_origin_ids": [1],
                            "list_of_speakers_id": 1,
                            "state_id": 1,
                        },
                    ),
                },
                "list_of_speakers": {
                    "1": {
                        "id": 1,
                        "meeting_id": 1,
                        "content_object_id": "motion/1",
                        "closed": False,
                        "sequential_number": 1,
                        "speaker_ids": [],
                        "projection_ids": [],
                    },
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["meeting"]["1"]["list_of_speakers_ids"] = [1]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert (
            "Motion all_origin_ids and all_derived_motion_ids should be empty."
            in response.json["message"]
        )

    def test_missing_required_field(self) -> None:
        request_data = self.create_request_data(
            {
                "motion": {
                    "1": self.get_motion_data(
                        1,
                        {
                            "all_origin_ids": [],
                            "list_of_speakers_id": None,
                            "state_id": 1,
                        },
                    ),
                },
            }
        )
        request_data["meeting"]["meeting"]["1"]["motion_ids"] = [1]
        request_data["meeting"]["motion_state"]["1"]["motion_ids"] = [1]
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert (
            "motion/1/list_of_speakers_id: Field required but empty."
            in response.json["message"]
        )

    def test_field_check(self) -> None:
        request_data = self.create_request_data(
            {
                "mediafile": {
                    "1": self.get_mediafile_data(
                        1,
                        {
                            "foobar": "test this",
                        },
                    ),
                }
            }
        )
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert (
            "mediafile/1: Invalid fields foobar (value: test this)"
            in response.json["message"]
        )

    def test_bad_format_invalid_id_key(self) -> None:
        request_data = self.create_request_data({"tag": {"1": {"id": 2}}})
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert "tag/1: Id must be the same as model['id']" in response.json["message"]

    def test_limit_of_meetings_error(self) -> None:
        self.update_model("organization/1", {"limit_of_meetings": 1})
        response = self.request("meeting.import", self.create_request_data({}))
        self.assert_status_code(response, 400)
        self.assertIn(
            "You cannot import an active meeting, because you reached your limit of 1 active meetings.",
            response.json["message"],
        )

    def test_limit_of_meetings_ok(self) -> None:
        self.update_model("organization/1", {"limit_of_meetings": 2})
        response = self.request("meeting.import", self.create_request_data({}))
        self.assert_status_code(response, 200)

    def test_check_limit_of_users_okay(self) -> None:
        self.set_models(
            {
                "organization/1": {"limit_of_users": 2},
            }
        )
        request_data = self.create_request_data({})
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 200)
        self.assert_model_exists("user/2")

    def test_check_hit_limit_of_users(self) -> None:
        self.set_models(
            {
                "organization/1": {"limit_of_users": 2},
                "user/2": {"username": "test2", "is_active": True},
            }
        )
        request_data = self.create_request_data({})
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        assert (
            "The number of active users cannot exceed the limit of users."
            == response.json["message"]
        )

    def test_check_forbidden_organization_management_right(self) -> None:
        request_data = self.create_request_data(
            {
                "user": {
                    "1": {
                        "organization_management_level": "superadmin",
                    }
                },
            }
        )
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        self.assertIn(
            "Imported user may not have OrganizationManagementLevel rights!",
            response.json["message"],
        )

    def test_check_forbidden_committee_management_right(self) -> None:
        request_data = self.create_request_data(
            {
                "user": {
                    "1": {
                        "committee_$_management_level": ["can_manage"],
                        "committee_$can_manage_management_level": [1],
                    }
                },
            }
        )
        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        self.assertIn(
            "Imported user may not have CommitteeManagementLevel rights!",
            response.json["message"],
        )

    def test_check_missing_admin_group_in_meeting(self) -> None:
        self.set_models(
            {
                "user/1": {"username": "admin"},
            }
        )
        request_data = self.create_request_data({})
        request_data["meeting"]["meeting"]["1"]["admin_group_id"] = None
        request_data["meeting"]["group"]["1"]["admin_group_for_meeting_id"] = None

        response = self.request("meeting.import", request_data)
        self.assert_status_code(response, 400)
        self.assertIn(
            "Imported meeting has no AdminGroup to assign to request user",
            response.json["message"],
        )

    def test_without_migration_index(self) -> None:
        data = self.create_request_data({})
        del data["meeting"]["_migration_index"]
        response = self.request("meeting.import", data)
        self.assert_status_code(response, 400)
        self.assertIn(
            "The data must have a valid migration index, but 'None' is not valid!",
            response.json["message"],
        )

    def test_with_negative_migration_index(self) -> None:
        data = self.create_request_data({})
        data["meeting"]["_migration_index"] = -1
        response = self.request("meeting.import", data)
        self.assert_status_code(response, 400)
        self.assertIn(
            "The data must have a valid migration index, but '-1' is not valid!",
            response.json["message"],
        )

    def test_with_migration_index_to_high(self) -> None:
        data = self.create_request_data({})
        data["meeting"]["_migration_index"] = 12345678
        response = self.request("meeting.import", data)
        self.assert_status_code(response, 400)
        self.assertIn(
            f"Your data migration index '12345678' is higher than the migration index of this backend '{current_migration_index}'! Please, update your backend!",
            response.json["message"],
        )

    def test_all_migrations(self) -> None:
        data = self.create_request_data({})
        data["meeting"]["_migration_index"] = 1
        response = self.request("meeting.import", data)
        self.assert_status_code(response, 200)
        self.assert_model_exists("user/1", {"group_$_ids": ["2"], "group_$2_ids": [2]})
        meeting = self.assert_model_exists(
            "meeting/2", {"assignment_poll_enable_max_votes_per_option": False}
        )  # checker repair
        self.assertCountEqual(meeting["user_ids"], [1, 2])
        group2 = self.assert_model_exists("group/2")
        self.assertCountEqual(group2["user_ids"], [1, 2])
        committee1 = self.get_model("committee/1")
        self.assertCountEqual(committee1["user_ids"], [1, 2])
        self.assertCountEqual(committee1["meeting_ids"], [1, 2])
        self.assert_model_exists("motion_workflow/1", {"sequential_number": 1})
        self.assert_model_exists("projector/2", {"sequential_number": 1})
