from typing import Any, Dict

from openslides_backend.permissions.permissions import Permissions
from tests.system.action.base import BaseActionTestCase


class MotionCreateForwarded(BaseActionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_model: Dict[str, Dict[str, Any]] = {
            "meeting/1": {
                "name": "name_XDAddEAW",
                "committee_id": 53,
                "is_active_in_organization_id": 1,
            },
            "meeting/2": {
                "name": "name_SNLGsvIV",
                "motions_default_workflow_id": 12,
                "committee_id": 52,
                "is_active_in_organization_id": 1,
                "default_group_id": 112,
                "group_ids": [112],
            },
            "user/1": {"meeting_ids": [1, 2]},
            "motion_workflow/12": {
                "name": "name_workflow1",
                "first_state_id": 34,
                "state_ids": [34],
            },
            "motion_state/34": {
                "name": "name_state34",
                "meeting_id": 2,
            },
            "motion_state/30": {
                "name": "name_UVEKGkwf",
                "meeting_id": 1,
                "allow_motion_forwarding": True,
            },
            "motion/12": {
                "title": "title_FcnPUXJB",
                "meeting_id": 1,
                "state_id": 30,
            },
            "committee/52": {"name": "name_EeKbwxpa"},
            "committee/53": {
                "name": "name_auSwgfJC",
                "forward_to_committee_ids": [52],
            },
            "group/112": {"name": "YZJAwUPK", "meeting_id": 2},
        }

    def test_correct_origin_id_set(self) -> None:
        self.set_models(self.test_model)
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "text": "test",
                "reason": "reason_jLvcgAMx",
            },
        )
        self.assert_status_code(response, 200)
        model = self.assert_model_exists(
            "motion/13",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "all_derived_motion_ids": [],
                "all_origin_ids": [12],
                "reason": "reason_jLvcgAMx",
                "submitter_ids": [1],
                "state_id": 34,
            },
        )
        assert model.get("forwarded")
        self.assert_model_exists(
            "motion_submitter/1",
            {
                "user_id": 2,
                "motion_id": 13,
            },
        )
        self.assert_model_exists(
            "user/2",
            {
                "username": "name_auSwgfJC",
                "is_physical_person": False,
                "is_active": False,
                "group_$_ids": ["2"],
                "group_$2_ids": [112],
                "forwarding_committee_ids": [53],
                "submitted_motion_$_ids": ["2"],
                "submitted_motion_$2_ids": [1],
            },
        )
        self.assert_model_exists("group/112", {"user_ids": [2]})
        self.assert_model_exists("committee/53", {"forwarding_user_id": 2})
        self.assert_model_exists(
            "motion/12", {"derived_motion_ids": [13], "all_derived_motion_ids": [13]}
        )

    def test_correct_existing_forward_user(self) -> None:
        self.set_models(self.test_model)
        self.set_models(
            {
                "user/2": {
                    "username": "name_EeKbwxpa",
                    "is_physical_person": False,
                    "is_active": False,
                    "group_$_ids": ["2"],
                    "group_$2_ids": [113],
                    "forwarding_committee_ids": [53],
                },
                "group/113": {"name": "HPMHcWhk", "meeting_id": 2, "user_ids": [2]},
                "meeting/2": {"group_ids": [112, 113]},
                "committee/53": {"forwarding_user_id": 2},
            }
        )

        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "text": "test",
                "reason": "reason_jLvcgAMx",
            },
        )
        self.assert_status_code(response, 200)
        model = self.assert_model_exists(
            "motion/13",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "all_derived_motion_ids": [],
                "all_origin_ids": [12],
                "reason": "reason_jLvcgAMx",
            },
        )
        assert model.get("forwarded")
        self.assert_model_exists(
            "user/2",
            {
                "username": "name_EeKbwxpa",
                "is_physical_person": False,
                "is_active": False,
                "group_$_ids": ["2"],
                "group_$2_ids": [113, 112],
                "forwarding_committee_ids": [53],
            },
        )
        self.assert_model_exists("group/112", {"user_ids": [2]})
        self.assert_model_exists("group/113", {"user_ids": [2]})
        self.assert_model_exists("committee/53", {"forwarding_user_id": 2})
        self.assert_model_exists(
            "motion/12", {"derived_motion_ids": [13], "all_derived_motion_ids": [13]}
        )

    def test_correct_origin_id_wrong_1(self) -> None:
        self.test_model["committee/53"]["forward_to_committee_ids"] = []
        self.set_models(self.test_model)
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "text": "text",
                "meeting_id": 2,
                "origin_id": 12,
            },
        )
        self.assert_status_code(response, 400)
        assert "Committee id 52 not in []" in response.json["message"]

    def test_missing_origin(self) -> None:
        self.set_models(
            {
                "meeting/222": {
                    "name": "meeting_222",
                    "is_active_in_organization_id": 1,
                },
            }
        )
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "text": "text",
                "meeting_id": 222,
                "origin_id": 12,
            },
        )
        self.assert_status_code(response, 400)
        assert "Model 'motion/12' does not exist." in response.json["message"]

    def test_all_origin_ids_complex(self) -> None:
        self.set_models(
            {
                "meeting/1": {
                    "name": "name_XDAddEAW",
                    "committee_id": 53,
                    "is_active_in_organization_id": 1,
                },
                "meeting/2": {
                    "name": "name_SNLGsvIV",
                    "motions_default_workflow_id": 12,
                    "committee_id": 52,
                    "is_active_in_organization_id": 1,
                    "default_group_id": 112,
                    "group_ids": [112],
                },
                "user/1": {"meeting_ids": [1, 2]},
                "motion_workflow/12": {
                    "name": "name_workflow1",
                    "first_state_id": 34,
                    "state_ids": [34],
                },
                "motion_state/34": {
                    "name": "name_state34",
                    "meeting_id": 2,
                    "allow_motion_forwarding": True,
                },
                "motion/6": {
                    "title": "title_FcnPUXJB layer 1",
                    "meeting_id": 1,
                    "state_id": 34,
                    "derived_motion_ids": [11, 12],
                    "all_origin_ids": [],
                    "all_derived_motion_ids": [11, 12, 13],
                },
                "motion/11": {
                    "title": "test11 layer 2",
                    "meeting_id": 1,
                    "state_id": 34,
                    "origin_id": 6,
                    "derived_motion_ids": [13],
                    "all_origin_ids": [6],
                    "all_derived_motion_ids": [13],
                },
                "motion/12": {
                    "title": "test12 layer 2",
                    "meeting_id": 1,
                    "state_id": 34,
                    "origin_id": 6,
                    "derived_motion_ids": [],
                    "all_origin_ids": [6],
                    "all_derived_motion_ids": [],
                },
                "motion/13": {
                    "title": "test13 layer 3",
                    "meeting_id": 1,
                    "state_id": 34,
                    "origin_id": 11,
                    "derived_motion_ids": [],
                    "all_origin_ids": [6, 11],
                    "all_derived_motion_ids": [],
                },
                "committee/52": {"name": "name_EeKbwxpa"},
                "committee/53": {
                    "name": "name_auSwgfJC",
                    "forward_to_committee_ids": [52],
                },
                "group/112": {"name": "YZJAwUPK", "meeting_id": 2},
            }
        )
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_XXX_leyer 3",
                "meeting_id": 2,
                "origin_id": 11,
                "text": "test",
            },
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "motion/14",
            {"origin_id": 11, "all_origin_ids": [6, 11], "all_derived_motion_ids": []},
        )
        self.assert_model_exists(
            "motion/13",
            {"origin_id": 11, "all_origin_ids": [6, 11], "all_derived_motion_ids": []},
        )
        self.assert_model_exists(
            "motion/12",
            {"origin_id": 6, "all_origin_ids": [6], "all_derived_motion_ids": []},
        )
        self.assert_model_exists(
            "motion/11",
            {"origin_id": 6, "all_origin_ids": [6], "all_derived_motion_ids": [13, 14]},
        )
        self.assert_model_exists(
            "motion/6",
            {
                "origin_id": None,
                "all_origin_ids": [],
                "all_derived_motion_ids": [11, 12, 13, 14],
            },
        )

    def test_not_allowed_to_forward_amendments(self) -> None:
        self.set_models(
            {
                "meeting/1": {
                    "name": "name_XDAddEAW",
                    "committee_id": 53,
                    "is_active_in_organization_id": 1,
                },
                "user/1": {"meeting_ids": [1, 2]},
                "motion/6": {
                    "title": "title_FcnPUXJB layer 1",
                    "meeting_id": 1,
                    "state_id": 34,
                    "derived_motion_ids": [],
                    "all_origin_ids": [],
                    "all_derived_motion_ids": [],
                },
                "motion/11": {
                    "title": "test11 layer 2",
                    "meeting_id": 1,
                    "state_id": 34,
                    "derived_motion_ids": [],
                    "all_origin_ids": [],
                    "all_derived_motion_ids": [],
                    "lead_motion_id": 6,
                },
                "motion_workflow/12": {
                    "name": "name_workflow1",
                    "first_state_id": 34,
                    "state_ids": [34],
                },
                "motion_state/34": {
                    "name": "name_state34",
                    "meeting_id": 1,
                },
            }
        )
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_foo",
                "meeting_id": 1,
                "origin_id": 11,
                "text": "test",
            },
        )
        self.assert_status_code(response, 403)
        assert "Amendments cannot be forwarded." in response.json["message"]

    def test_create_forwarded_not_allowed_by_state(self) -> None:
        self.test_model["motion_state/30"]["allow_motion_forwarding"] = False
        self.set_models(self.test_model)
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "text": "test",
            },
        )
        self.assert_status_code(response, 400)
        assert "State doesn't allow to forward motion." in response.json["message"]

    def test_no_permissions(self) -> None:
        self.create_meeting()
        self.user_id = self.create_user("user")
        self.login(self.user_id)
        self.set_models({"group/4": {"meeting_id": 2}})
        self.set_user_groups(self.user_id, [3, 4])
        self.set_models(self.test_model)
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "text": "test",
            },
        )
        self.assert_status_code(response, 403)
        assert "Missing permission: motion.can_forward" in response.json["message"]

    def test_permissions(self) -> None:
        self.create_meeting()
        self.user_id = self.create_user("user")
        self.login(self.user_id)
        self.set_models({"group/4": {"meeting_id": 2}})
        self.set_user_groups(self.user_id, [3, 4])
        self.set_models(self.test_model)
        self.set_group_permissions(3, [Permissions.Motion.CAN_MANAGE])
        self.set_group_permissions(4, [Permissions.Motion.CAN_FORWARD])
        response = self.request(
            "motion.create_forwarded",
            {
                "title": "test_Xcdfgee",
                "meeting_id": 2,
                "origin_id": 12,
                "text": "test",
            },
        )
        self.assert_status_code(response, 200)
