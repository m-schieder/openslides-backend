from openslides_backend.permissions.management_levels import OrganizationManagementLevel
from tests.system.action.base import BaseActionTestCase


class ThemeCreateActionTest(BaseActionTestCase):
    def test_create(self) -> None:
        self.create_model("organization/1")
        response = self.request(
            "theme.create",
            {
                "name": "test_Xcdfgee",
                "primary_500": "#111222",
                "accent_500": "#111222",
                "warn_500": "#222333",
            },
        )
        self.assert_status_code(response, 200)
        self.assert_model_exists(
            "theme/1",
            {
                "name": "test_Xcdfgee",
                "primary_500": "#111222",
                "accent_500": "#111222",
                "warn_500": "#222333",
                "organization_id": 1,
            },
        )

    def test_create_empty_data(self) -> None:
        response = self.request("theme.create", {})
        self.assert_status_code(response, 400)
        self.assertIn(
            "data must contain ['name', 'primary_500', 'accent_500', 'warn_500'] properties",
            response.json["message"],
        )

    def test_create_permission(self) -> None:
        self.base_permission_test(
            {},
            "theme.create",
            {
                "name": "test_Xcdfgee",
                "primary_500": "#111222",
                "accent_500": "#111222",
                "warn_500": "#222333",
            },
            OrganizationManagementLevel.CAN_MANAGE_ORGANIZATION,
        )

    def test_create_no_permission(self) -> None:
        self.base_permission_test(
            {},
            "theme.create",
            {
                "name": "test_Xcdfgee",
                "primary_500": "#111222",
                "accent_500": "#111222",
                "warn_500": "#222333",
            },
        )
