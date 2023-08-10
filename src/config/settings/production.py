from config.settings.base import *  # NOQA

DEBUG = False

SECRET_KEY = "django-insecure-56s@6_c#(vnnq$ex9g03@bui)!s&^mr7@gt&jrem=&i)zbll9s"

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

STATIC_URL = "static/"
