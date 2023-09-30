import os

from config.settings.base import *  # NOQA

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["localhost", "ec2-16-170-238-29.eu-north-1.compute.amazonaws.com"]

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": os.environ.get("POSTGRES_DB"),
    #     "USER": os.environ.get("POSTGRES_USER"),
    #     "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    #     "HOST": os.environ.get("POSTGRES_HOST"),
    #     "PORT": os.environ.get("POSTGRES_PORT"),
    # }
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = BASE_DIR / "static_content/"  # NOQA
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media_content/"  # NOQA
MEDIA_URL = "/media/"