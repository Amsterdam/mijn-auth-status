import json
import os
from datetime import datetime, timedelta, timezone
from math import floor

from freezegun import freeze_time
from tma_saml.for_tests.cert_and_key import server_crt

from tma_saml.for_tests.fixtures import generate_saml_token_for_bsn, generate_tampered_saml_token_, \
    generate_saml_token_for_kvk

# override env before authserver.service.config is imported anywhere
os.environ['TMA_CERTIFICATE'] = server_crt

from authstatus.server import application


def test_check_operation_unauthenticated():
    client = application.test_client()
    response = client.get('/auth/check')
    data = json.loads(response.get_data(as_text=True))
    assert data == {
        'isAuthenticated': False
    }
    assert response.status_code == 200


def test_check_operation_burger():
    client = application.test_client()

    now = datetime.now(tz=timezone.utc)
    valid_until = now + timedelta(minutes=15)

    with freeze_time(now):
        token = generate_saml_token_for_bsn('987654329')
        headers = {'x-saml-attribute-token1': token}

        response = client.get('/auth/check', headers=headers)

        data = json.loads(response.get_data(as_text=True))

    # decrease resolution
    valid_until_timestamp_in_ms = floor(valid_until.timestamp() * 1000)

    assert data == {
        'isAuthenticated': True,
        'userType': "BURGER",
        "validUntil": floor(valid_until_timestamp_in_ms)
    }
    assert response.status_code == 200


def test_check_operation_fails_invalid_bsn():
    client = application.test_client()
    token = generate_saml_token_for_bsn('987654321')
    headers = {'x-saml-attribute-token1': token}

    response = client.get('/auth/check', headers=headers)
    assert 'Ongeldige BSN' in response.get_data(as_text=True)
    assert response.status_code == 400


def test_check_operation_fails_tampered_saml():
    client = application.test_client()
    token = generate_tampered_saml_token_('987654329', '987654321')

    headers = {
        'x-saml-attribute-token1': token
    }

    response = client.get('/auth/check', headers=headers)
    assert 'Access denied' in response.get_data(as_text=True)
    assert response.status_code == 403


def test_check_operation_company():
    client = application.test_client()

    # now = datetime.utcnow()
    # not_on_or_after_expected = now + timedelta(minutes=15)

    token = generate_saml_token_for_kvk('1235')
    headers = {'x-saml-attribute-token1': token}

    response = client.get('/auth/check', headers=headers)

    data = json.loads(response.get_data(as_text=True))
    assert data == {
        'isAuthenticated': True,
        'userType': "BEDRIJF",
        'validUntil': data['validUntil'],  # TODO: allow for testing the validity dates
    }
    assert response.status_code == 200


def test_health_operation():
    client = application.test_client()
    response = client.get('/auth/status/health')
    assert response.get_data(as_text=True) == '"OK"\n'
    assert response.status_code == 200
