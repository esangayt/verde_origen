from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5431',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# STATICFILES_DIRS = [BASE_DIR.child('static')]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
# MEDIA_ROOT = BASE_DIR.child('media')

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child('staticfiles')
STATICFILES_DIRS = [BASE_DIR.child('static')]

# print(BASE_DIR.child("djangoProjects").child("locale"))
#
# LOCALE_PATHS = [
#     BASE_DIR.child("djangoProjects").child("locale")
# ]
