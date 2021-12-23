from datetime import datetime, timedelta, timezone
from math import floor
from unittest.mock import patch

from freezegun import freeze_time
from tma_saml import FlaskServerTMATestCase
from tma_saml.for_tests.cert_and_key import server_crt
from tma_saml.for_tests.fixtures import (
    generate_saml_token_for_bsn,
    generate_saml_token_for_kvk,
    generate_tampered_saml_token_,
)

from app.server import app


@patch("app.helpers.get_tma_certificate", lambda: server_crt)
class ApiTests(FlaskServerTMATestCase):
    TEST_BSN = "111222333"

    def setUp(self):
        self.client = self.get_tma_test_app(app)
        self.maxDiff = None

    def saml_headers(self):
        return self.add_digi_d_headers(self.TEST_BSN)

    def get_secure(self, location):
        return self.client.get(location, headers=self.saml_headers())

    def test_check_operation_unauthenticated(self):
        response = self.client.get("/auth/check")
        response_data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data["status"], "ERROR")
        self.assertEqual(response_data["message"], "Not authenticated by TMA")
        self.assertEqual("content" not in response_data, True)

    def test_check_operation_burger(self):
        now = datetime.now(tz=timezone.utc)
        valid_until = now + timedelta(minutes=15)

        with freeze_time(now):
            response = self.get_secure("/auth/check")
            response_data = response.get_json()

        # decrease resolution
        valid_until_timestamp_in_ms = floor(valid_until.timestamp() * 1000)

        self.assertEqual(response_data["status"], "OK")
        self.assertEqual(
            response_data["content"],
            {
                "isAuthenticated": True,
                "userType": "BURGER",
                "validUntil": floor(valid_until_timestamp_in_ms),
            },
        )
        assert response.status_code == 200

    def test_check_operation_fails_invalid_bsn(self):
        token = generate_saml_token_for_bsn("987654321")
        headers = {"x-saml-attribute-token1": token}

        response = self.client.get("/auth/check", headers=headers)
        response_data = response.get_json()

        self.assertEqual("Not authenticated by TMA", response_data["message"])
        self.assertEqual(response.status_code, 401)

    def test_check_operation_fails_tampered_saml(self):
        token = generate_tampered_saml_token_("987654329", "987654321")
        headers = {"x-saml-attribute-token1": token}

        response = self.client.get("/auth/check", headers=headers)
        response_data = response.get_json()

        self.assertEqual("Not authenticated by TMA", response_data["message"])
        self.assertEqual(response.status_code, 401)

    def test_check_operation_company(self):

        now = datetime.now(tz=timezone.utc)
        valid_until = now + timedelta(minutes=15)

        token = generate_saml_token_for_kvk("1235")
        headers = {"x-saml-attribute-token1": token}

        with freeze_time(now):
            response = self.client.get("/auth/check", headers=headers)
            response_data = response.get_json()

        self.assertEqual(
            response_data["content"],
            {
                "isAuthenticated": True,
                "userType": "BEDRIJF",
                "validUntil": floor(valid_until.timestamp() * 1000),
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_status(self):
        response = self.client.get("/status/health")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["content"], "OK")
