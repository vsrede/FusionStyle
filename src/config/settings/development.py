import os

from config.settings.base import *  # NOQA

DEBUG = True

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        },
    }
else:
    DATABASES = {
        # local
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "vladyslav_oriekhov",
            "USER": "vladyslav",
            "PASSWORD": "admin",
            "HOST": "localhost",
            "PORT": 5432,
        },
        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "NAME": os.environ.get("POSTGRES_DB"),
        #     "USER": os.environ.get("POSTGRES_USER"),
        #     "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        #     "HOST": os.environ.get("POSTGRES_HOST"),
        #     "PORT": os.environ.get("POSTGRES_PORT"),
        # }
    }

STATIC_ROOT = BASE_DIR / "static/"  # NOQA
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media/"  # NOQA
MEDIA_URL = "/media/"
