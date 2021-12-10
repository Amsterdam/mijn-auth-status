import logging

import sentry_sdk
from flask import Flask
from requests.exceptions import HTTPError
from sentry_sdk.integrations.flask import FlaskIntegration
from tma_saml.user_type import UserType

from app.auth_service import get_user_info
from app.config import IS_DEV, CustomJSONEncoder, TMAException, get_sentry_dsn
from app.helpers import (
    error_response_json,
    get_tma_user,
    success_response_json,
    validate_openapi,
    verify_tma_user,
)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

sentry_dsn = get_sentry_dsn()
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn, integrations=[FlaskIntegration()], with_locals=False
    )


@app.route("/auth/check", methods=["GET"])
@verify_tma_user
@validate_openapi
def auth_check():
    user = get_tma_user()
    user_info = get_user_info(user)
    return success_response_json(user_info)


@app.route("/status/health")
def health_check():
    return success_response_json("OK")


@app.errorhandler(Exception)
def handle_error(error):

    error_message_original = str(error)

    msg_tma_exception = "Not authenticated by TMA"
    msg_request_http_error = "Request error occurred"
    msg_server_error = "Server error occurred"

    if not app.config["TESTING"]:
        logging.exception(
            error, extra={"error_message_original": error_message_original}
        )

    if IS_DEV:
        msg_tma_exception = error_message_original
        msg_request_http_error = error_message_original
        msg_server_error = error_message_original

    if isinstance(error, HTTPError):
        return error_response_json(
            msg_request_http_error,
            error.response.status_code,
        )
    elif isinstance(error, TMAException):
        return error_response_json(msg_tma_exception, 401)

    return error_response_json(msg_server_error, 500)


if __name__ == "__main__":
    app.run()
