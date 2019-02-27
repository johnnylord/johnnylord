from .base import *

from decouple import config, Csv


# Allowed host
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# EMAIL BACKEND SETTING
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
