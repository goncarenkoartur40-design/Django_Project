from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

SECRET_KEY = '$l@2fz5idja=s&cqqenewf4v@od0ag#956_#*1jn-i00#h#i$x'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

