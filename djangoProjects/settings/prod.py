import os
import sys

import dj_database_url

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

DEBUG = config("DEBUG", False, cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DEVELOPMENT_MODE = config("DEVELOPMENT_MODE", False, cast=bool)

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR.child("db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if config("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child('staticfiles')
STATICFILES_DIRS = [BASE_DIR.child('static')]
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR.child('media')

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
