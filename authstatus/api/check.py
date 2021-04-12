import math
from datetime import datetime, timedelta, timezone

import connexion
from flask import request
from tma_saml import get_user_type

from authstatus.service.config import TMA_CERTIFICATE

from authstatus.service.logging import log_request, log_and_generate_response


def search():
    try:
        log_request(request)
        saml_token = connexion.request.headers.get('x-saml-attribute-token1')
        if saml_token:
            # Fails on invalid cert or missing KvK & invalid BSN
            user_type = get_user_type(connexion.request, TMA_CERTIFICATE)

            # TMA sessions are valid for 15 minutes
            validity_datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
            # Timestamp in whole milliseconds (because that's what Javascript wants)
            timestamp = math.floor(validity_datetime.timestamp() * 1000)

            return {
                "isAuthenticated": True,
                "userType": user_type.value,
                "validUntil": timestamp,
            }

        return {
            "isAuthenticated": False
        }
    except Exception as e:
        return log_and_generate_response(e)
