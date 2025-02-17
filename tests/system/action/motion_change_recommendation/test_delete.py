from typing import Any, Dict

from openslides_backend.permissions.permissions import Permissions
from tests.system.action.base import BaseActionTestCase


class MotionChangeRecommendationActionTest(BaseActionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.permission_test_models: Dict[str, Dict[str, Any]] = {
            "motion_change_recommendation/111": {"meeting_id": 1}
        }

    def test_delete_correct(self) -> None:
        self.set_models(
            {
                "motion_change_recommendation/111": {"meeting_id": 1},
                "meeting/1": {"is_active_in_organization_id": 1},
            }
        )
        response = self.request("motion_change_recommendation.delete", {"id": 111})
        self.assert_status_code(response, 200)
        self.assert_model_deleted("motion_change_recommendation/111")

    def test_delete_wrong_id(self) -> None:
        self.set_models(
            {
                "motion_change_recommendation/112": {"meeting_id": 1},
                "meeting/1": {"is_active_in_organization_id": 1},
            }
        )
        response = self.request("motion_change_recommendation.delete", {"id": 111})
        self.assert_status_code(response, 400)
        self.assert_model_exists("motion_change_recommendation/112")

    def test_delete_no_permission(self) -> None:
        self.base_permission_test(
            self.permission_test_models,
            "motion_change_recommendation.delete",
            {"id": 111},
        )

    def test_delete_permission(self) -> None:
        self.base_permission_test(
            self.permission_test_models,
            "motion_change_recommendation.delete",
            {"id": 111},
            Permissions.Motion.CAN_MANAGE,
        )
