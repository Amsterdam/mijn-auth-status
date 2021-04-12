import logging

from connexion.resolver import RestyResolver
from sentry_sdk.integrations.flask import FlaskIntegration
import connexion
import sentry_sdk

from authstatus.service.config import SENTRY_DSN

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        with_locals=True
    )

logging.basicConfig(level=logging.INFO)
webapp = connexion.App(
    __name__,
    specification_dir='swagger/'
)

# using a custom resolver to determine operations
# instead of the operationId in the yaml file.
webapp.add_api(
    'main.json',
    resolver=RestyResolver('api'),
    validate_responses=True
)

# set the WSGI application callable to allow using uWSGI:
application = webapp.app


if __name__ == "__main__":
    webapp.run(port=8765)
