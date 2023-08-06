import os

SECRET_KEY = "test_frontend_vue"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = [
    "tests",
    "gdaps.frontend",
    "gdaps",
]

#ROOT_URLCONF =
GDAPS = {"FRONTEND_ENGINE": "vue"}
