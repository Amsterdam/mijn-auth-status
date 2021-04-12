import logging

# Add variables to current module scope
from tma_saml import InvalidBSNException, SamlVerificationException

# End config hack
from .exceptions import ServiceException, unkown_error


def log_and_generate_response(exception):
    logging.error("exception: %s" % exception)
    e_type = type(exception)
    if e_type == ServiceException:
        return exception.to_dict(), 500
    elif e_type == SamlVerificationException:
        return 'Access denied', 403
    elif e_type == InvalidBSNException:
        return 'Ongeldige BSN', 400
    else:
        return unkown_error().to_dict(), 500


def log_request(req):
    logging.info(req.url)
