from flask import request
from authstatus.service.logging import log_request, log_and_generate_response


def get():
    """
    Health check
    """
    try:
        log_request(request)
        return 'OK'
    except Exception as e:
        return log_and_generate_response(e)
