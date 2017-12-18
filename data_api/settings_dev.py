from .settings_common import *

SECRET_KEY = '5fde38c8-b49b-11e7-800e-3c970e7be43b'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rapidpro_data_api',
        'USER': 'postgres',
        'HOST': 'localhost',
    }
}


RAVEN_CONFIG = {}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
             'level': 'ERROR',
             'filters': [],
             'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'WARNING',
        },
        'scheduling': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
