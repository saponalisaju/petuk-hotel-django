import os
from pathlib import Path

# BASE_DIR → project root (django-ecommerce/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Helpers
def get_bool(name: str, default: str = "False") -> bool:
    return os.environ.get(name, default).strip().lower() in {"true", "1", "yes", "on"}

def get_required(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val

def split_csv(name: str, default: str = "") -> list[str]:
    raw = os.environ.get(name, default)
    return [i.strip() for i in raw.split(",") if i.strip()]

DEBUG = os.environ.get("DEBUG", default=False)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


LANGUAGE_CODE = "bn"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party
    "taggit",
    "django_ckeditor_5",
    "easyaudit",

    # custom apps
    "core",
    "userauths",
    "blog",

    # cloudinary
    "cloudinary",
    "cloudinary_storage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecomproject.urls"
WSGI_APPLICATION = "ecomproject.wsgi.application"
ASGI_APPLICATION = "ecomproject.asgi.application"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # project root/templates/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = 'userauths:sign-in'  # check spelling in your urls.py

AUTH_USER_MODEL = 'userauths.User'

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'link', 'underline', 'strikethrough', '|',
            'bulletedList', 'numberedList', 'blockQuote', '|',
            'insertTable', 'mediaEmbed', 'undo', 'redo', 'imageUpload'
        ],
        'height': 300,
        'width': '100%',
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# settings/base.py বা utils.py
SITE_SCHEME = os.environ.get("SITE_SCHEME", "https")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost:8000")

def abs_url(path: str) -> str:
    return f"{SITE_SCHEME}://{SITE_DOMAIN}{path}"

