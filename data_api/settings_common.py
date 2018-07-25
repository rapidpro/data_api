__author__ = 'kenneth'
"""
Django settings for data_api project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'anymail',

    'data_api.api',
    'data_api.sql_views',
    'data_api.staging',
    'data_api.staging_api',
    'data_api.ui',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_mongoengine',
    'rest_framework_swagger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'data_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'data_api.wsgi.application'

RAPIDPRO_DEFAULT_SITE = 'https://app.rapidpro.io/'
RAPIDPRO_USE_ARCHIVES = False

LOG_FORMAT = '%(asctime)-15s %(message)s'

REST_FRAMEWORK = {
    'PAGINATE_BY': 10,                 # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 1000,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


RETRY_MAX_ATTEMPTS = int(os.environ.get('RETRY_MAX_ATTEMPTS', 10))
RETRY_WAIT_FIXED = int(os.environ.get('RETRY_WAIT_FIXED', 15*60*1000))

CELERY_BROKER_URL = 'redis://'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'data',
        'USER': 'postgres',
        'HOST': 'localhost',
    }
}


RAVEN_URL = None  # override WITH https://<key>:<secret>@app.getsentry.com/<project> to enable raven
RAVEN_CONFIG = {
    'dsn': 'https://<key>:<secret>@app.getsentry.com/<project>',
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR+'/static/'

ADMIN = (
    ('Admin', 'code@uniceflabs.org'),
)


ANYMAIL = {
    "MAILGUN_API_KEY": "****",
    "MAILGUN_SENDER_DOMAIN": 'mail.unicef.io',  # your Mailgun domain, if needed
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = 'Data Team <postmaster@mail.unicef.io>'
EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
SERVER_EMAIL = DEFAULT_FROM_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
                 '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
             'level': 'ERROR',
             'filters': ['require_debug_false'],
             'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
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

SITE_ID = 1

SWAGGER_SETTINGS = {
    'api_version': '0.1',
    'enabled_methods': [
        'get'
    ],
},

EXCLUDED_FLOWS = '55b99f354439f1187a6df178'

MAX_RECORDS_PER_EXPORT = 5000
CSV_DUMPS_FOLDER = '/mnt/data1/csv_dumps'
DEFAULT_ORG = '578c88f64439f1157befb2c6'
DEFAULT_MESSAGE_ATTRIBUTES = ['created_on', 'text', 'direction', 'status', 'sent_on', 'type']
DEFAULT_CONTACT_FIELDS = ['uuid', 'age_groups', 'education_level', 'village', 'occupation', 'district', 'year_born',
                              'registration_date', 'subcounty', 'gender', 'age', 'village_name', 'isfacebookuser',
                              'istwitteruser', 'isinternetuser', 'recruitment_source']


MONGO_DBNAME = 'rapidpro'
LOGIN_URL = '/admin/login/'
