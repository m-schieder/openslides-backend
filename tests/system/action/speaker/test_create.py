from typing import Any, Dict

from openslides_backend.permissions.permissions import Permissions
from tests.system.action.base import BaseActionTestCase

DEFAULT_PASSWORD = "password"


class SpeakerCreateActionTest(BaseActionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_models: Dict[str, Dict[str, Any]] = {
            "meeting/1": {"name": "name_asdewqasd", "is_active_in_organization_id": 1},
            "user/7": {
                "username": "test_username1",
                "meeting_ids": [1],
                "is_active": True,
                "default_password": DEFAULT_PASSWORD,
                "password": self.auth.hash(DEFAULT_PASSWORD),
            },
            "list_of_speakers/23": {"speaker_ids": [], "meeting_id": 1},
        }

    def test_create(self) -> None:
        self.set_models(self.test_models)
        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "speaker/1",
            {
                "user_id": 7,
                "list_of_speakers_id": 23,
                "weight": 1,
            },
        )
        self.assert_model_exists("list_of_speakers/23", {"speaker_ids": [1]})
        self.assert_model_exists(
            "user/7", {"speaker_$1_ids": [1], "speaker_$_ids": ["1"]}
        )

    def test_create_in_closed_los(self) -> None:
        self.test_models["list_of_speakers/23"]["closed"] = True
        self.set_models(self.test_models)

        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "speaker/1",
            {
                "user_id": 7,
                "list_of_speakers_id": 23,
                "weight": 1,
            },
        )
        self.assert_model_exists("list_of_speakers/23", {"speaker_ids": [1]})
        self.assert_model_exists(
            "user/7", {"speaker_$1_ids": [1], "speaker_$_ids": ["1"]}
        )

    def test_create_oneself_in_closed_los(self) -> None:
        self.test_models["list_of_speakers/23"]["closed"] = True
        self.test_models["group/1"] = {
            "meeting_id": 1,
            "name": "g1",
            "permissions": [
                Permissions.ListOfSpeakers.CAN_BE_SPEAKER,
            ],
        }
        self.set_models(self.test_models)
        self.set_user_groups(7, [1])
        self.user_id = 7
        self.login(self.user_id)
        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 400)
        self.assertIn("The list of speakers is closed.", response.json["message"])

    def test_create_oneself_in_closed_los_with_los_CAN_MANAGE(self) -> None:
        self.test_models["list_of_speakers/23"]["closed"] = True
        self.test_models["group/1"] = {
            "meeting_id": 1,
            "name": "g1",
            "permissions": [
                Permissions.ListOfSpeakers.CAN_MANAGE,
                Permissions.ListOfSpeakers.CAN_BE_SPEAKER,
            ],
        }
        self.set_models(self.test_models)
        self.set_user_groups(7, [1])
        self.user_id = 7
        self.login(self.user_id)
        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 200)

    def test_create_empty_data(self) -> None:
        response = self.request("speaker.create", {})
        self.assert_status_code(response, 400)
        self.assertIn(
            "data must contain ['list_of_speakers_id', 'user_id'] properties",
            response.json["message"],
        )

    def test_create_wrong_field(self) -> None:
        response = self.request("speaker.create", {"wrong_field": "text_AefohteiF8"})
        self.assert_status_code(response, 400)
        self.assertIn(
            "data must contain ['list_of_speakers_id', 'user_id'] properties",
            response.json["message"],
        )

    def test_create_already_exist(self) -> None:
        self.test_models["list_of_speakers/23"]["speaker_ids"] = [42]
        self.set_models(
            {
                **self.test_models,
                "speaker/42": {
                    "user_id": 7,
                    "list_of_speakers_id": 23,
                    "meeting_id": 1,
                },
            }
        )
        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 400)
        self.assertIn(
            "User 7 is already on the list of speakers.",
            response.json["message"],
        )
        list_of_speakers = self.get_model("list_of_speakers/23")
        assert list_of_speakers.get("speaker_ids") == [42]

    def test_create_add_2_speakers_in_1_action(self) -> None:
        self.set_models(
            {
                "meeting/1": {"is_active_in_organization_id": 1},
                "list_of_speakers/23": {"meeting_id": 1},
            }
        )
        response = self.request_multi(
            "speaker.create",
            [
                {"user_id": 1, "list_of_speakers_id": 23},
                {"user_id": 2, "list_of_speakers_id": 23},
            ],
        )
        self.assert_status_code(response, 400)
        self.assertIn(
            "It is not permitted to create more than one speaker per request!",
            response.json["message"],
        )

    def test_create_add_2_speakers_in_2_actions(self) -> None:
        self.set_models(
            {
                "meeting/7844": {
                    "is_active_in_organization_id": 1,
                },
                "user/7": {"meeting_ids": [7844]},
                "user/8": {"meeting_ids": [7844]},
                "user/9": {"meeting_ids": [7844]},
                "speaker/1": {"user_id": 7, "list_of_speakers_id": 23, "weight": 10000},
                "list_of_speakers/23": {"speaker_ids": [1], "meeting_id": 7844},
            }
        )
        response = self.request_json(
            [
                {
                    "action": "speaker.create",
                    "data": [
                        {"user_id": 8, "list_of_speakers_id": 23},
                    ],
                },
                {
                    "action": "speaker.create",
                    "data": [
                        {"user_id": 9, "list_of_speakers_id": 23},
                    ],
                },
            ],
        )
        self.assert_status_code(response, 400)
        self.assertIn(
            "Datastore service sends HTTP 400. The following locks were broken: 'speaker/list_of_speakers_id', 'speaker/meeting_id', 'speaker/weight'",
            response.json["message"],
        )

    def test_create_user_present(self) -> None:
        self.set_models(
            {
                "meeting/7844": {
                    "name": "name_asdewqasd",
                    "list_of_speakers_present_users_only": True,
                    "is_active_in_organization_id": 1,
                },
                "user/9": {
                    "username": "user9",
                    "speaker_$7844_ids": [3],
                    "speaker_$_ids": ["7844"],
                    "is_present_in_meeting_ids": [7844],
                    "meeting_ids": [7844],
                },
                "list_of_speakers/23": {"speaker_ids": [], "meeting_id": 7844},
            }
        )
        response = self.request(
            "speaker.create",
            {
                "user_id": 9,
                "list_of_speakers_id": 23,
            },
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists("speaker/1")

    def test_create_user_not_present(self) -> None:
        self.set_models(
            {
                "meeting/7844": {
                    "name": "name_asdewqasd",
                    "list_of_speakers_present_users_only": True,
                    "is_active_in_organization_id": 1,
                },
                "user/9": {
                    "username": "user9",
                    "speaker_$7844_ids": [3],
                    "speaker_$_ids": ["7844"],
                    "meeting_ids": [7844],
                },
                "list_of_speakers/23": {"speaker_ids": [], "meeting_id": 7844},
            }
        )
        response = self.request(
            "speaker.create",
            {
                "user_id": 9,
                "list_of_speakers_id": 23,
            },
        )
        self.assert_status_code(response, 400)
        self.assert_model_not_exists("speaker/1")
        self.assertIn(
            "Only present users can be on the lists of speakers.",
            response.json["message"],
        )

    def test_create_standard_speaker_in_only_talker_list(self) -> None:
        self.set_models(
            {
                "meeting/7844": {
                    "name": "name_asdewqasd",
                    "is_active_in_organization_id": 1,
                },
                "user/1": {"meeting_ids": [7844]},
                "user/7": {"username": "talking", "meeting_ids": [7844]},
                "speaker/1": {
                    "user_id": 7,
                    "list_of_speakers_id": 23,
                    "begin_time": 100000,
                    "weight": 5,
                    "meeting_id": 7844,
                },
                "list_of_speakers/23": {"speaker_ids": [1], "meeting_id": 7844},
            }
        )
        response = self.request(
            "speaker.create", {"user_id": 1, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "speaker/2",
            {"user_id": 1, "weight": 1},
        )
        self.assert_model_exists("list_of_speakers/23", {"speaker_ids": [1, 2]})

    def test_create_standard_speaker_at_the_end_of_filled_list(self) -> None:
        self.set_models(
            {
                "meeting/7844": {
                    "name": "name_asdewqasd",
                    "is_active_in_organization_id": 1,
                },
                "user/7": {"username": "talking", "meeting_ids": [7844]},
                "user/8": {"username": "waiting", "meeting_ids": [7844]},
                "user/1": {
                    "speaker_$7844_ids": [3],
                    "speaker_$_ids": ["7844"],
                    "meeting_ids": [7844],
                },
                "speaker/1": {
                    "user_id": 7,
                    "list_of_speakers_id": 23,
                    "begin_time": 100000,
                    "weight": 5,
                    "meeting_id": 7844,
                },
                "speaker/2": {
                    "user_id": 8,
                    "list_of_speakers_id": 23,
                    "weight": 1,
                    "meeting_id": 7844,
                },
                "speaker/3": {
                    "user_id": 1,
                    "list_of_speakers_id": 23,
                    "point_of_order": True,
                    "weight": 2,
                    "meeting_id": 7844,
                },
                "list_of_speakers/23": {"speaker_ids": [1, 2, 3], "meeting_id": 7844},
            }
        )
        response = self.request(
            "speaker.create", {"user_id": 1, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "speaker/3",
            {"user_id": 1, "point_of_order": True, "weight": 2},
        )
        self.assert_model_exists(
            "speaker/4",
            {"user_id": 1, "point_of_order": None, "weight": 3},
        )
        self.assert_model_exists("list_of_speakers/23", {"speaker_ids": [1, 2, 3, 4]})

    def test_create_not_in_meeting(self) -> None:
        self.set_models(
            {
                "meeting/1": {"is_active_in_organization_id": 1},
                "meeting/2": {"is_active_in_organization_id": 1},
                "user/7": {"meeting_ids": [1]},
                "list_of_speakers/23": {"speaker_ids": [], "meeting_id": 2},
            }
        )
        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 400)

    def test_create_note_and_not_point_of_order(self) -> None:
        self.set_models(self.test_models)
        response = self.request(
            "speaker.create",
            {"user_id": 7, "list_of_speakers_id": 23, "note": "blablabla"},
        )
        self.assert_status_code(response, 400)
        assert (
            "Not allowed to set note if not point of order." in response.json["message"]
        )

    def test_create_no_permissions(self) -> None:
        self.base_permission_test(
            self.test_models,
            "speaker.create",
            {"user_id": 7, "list_of_speakers_id": 23},
        )

    def test_create_permissions(self) -> None:
        self.base_permission_test(
            self.test_models,
            "speaker.create",
            {"user_id": 7, "list_of_speakers_id": 23},
            Permissions.ListOfSpeakers.CAN_MANAGE,
        )

    def test_create_permissions_selfadd(self) -> None:
        self.create_meeting()
        self.user_id = 7
        self.set_models(self.test_models)
        self.login(self.user_id)
        self.set_user_groups(self.user_id, [3])
        self.set_group_permissions(3, [Permissions.ListOfSpeakers.CAN_BE_SPEAKER])
        response = self.request(
            "speaker.create", {"user_id": 7, "list_of_speakers_id": 23}
        )
        self.assert_status_code(response, 200)

    def base_state_speech_test(
        self,
        status_code: int,
        speech_state: str,
        self_contribution: bool = True,
        pro_contra: bool = True,
        assert_message: str = "",
    ) -> None:
        self.create_meeting()
        self.user_id = self.create_user("user")
        self.login(self.user_id)
        self.set_user_groups(self.user_id, [3])
        self.set_group_permissions(3, [Permissions.ListOfSpeakers.CAN_MANAGE])
        self.test_models["meeting/1"][
            "list_of_speakers_enable_pro_contra_speech"
        ] = pro_contra
        self.test_models["meeting/1"][
            "list_of_speakers_can_set_contribution_self"
        ] = self_contribution
        self.set_models(self.test_models)
        response = self.request(
            "speaker.create",
            {"user_id": 7, "list_of_speakers_id": 23, "speech_state": speech_state},
        )
        self.assert_status_code(response, status_code)
        assert assert_message in response.json["message"]

    def test_create_pro_contra(self) -> None:
        self.base_state_speech_test(200, "pro", False, True)

    def test_create_contradiction(self) -> None:
        self.base_state_speech_test(200, "contribution")

    def test_create_contradiction_2(self) -> None:
        self.base_state_speech_test(200, "contribution", False)

    def test_create_not_allowed_pro_contra(self) -> None:
        self.base_state_speech_test(
            400, "pro", False, False, "Pro/Contra is not enabled."
        )

    def test_create_not_allowed_contribution(self) -> None:
        self.create_meeting()
        self.user_id = self.create_user("user")
        self.login(self.user_id)
        self.set_user_groups(self.user_id, [3])
        self.set_group_permissions(3, [Permissions.ListOfSpeakers.CAN_BE_SPEAKER])
        self.set_models(self.test_models)
        response = self.request(
            "speaker.create",
            {
                "user_id": self.user_id,
                "list_of_speakers_id": 23,
                "speech_state": "contribution",
            },
        )
        self.assert_status_code(response, 400)
        assert "Self contribution is not allowed" in response.json["message"]
