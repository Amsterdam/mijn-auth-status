from logging import config

import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


TMA_CERTIFICATE = os.getenv('TMA_CERTIFICATE')

assert (TMA_CERTIFICATE is not None)

DEBUG = os.getenv("DEBUG", 'False') == 'True'

SENTRY_DSN = os.getenv('SENTRY_DSN', None)


def debug_logging():
    config.dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'zeep.transports': {
                'level': 'DEBUG',
                'propagate': True,
                'handlers': ['console'],
            },
        }
    })


if DEBUG:
    debug_logging()
