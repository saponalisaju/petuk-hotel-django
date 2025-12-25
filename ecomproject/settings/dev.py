# ecomproject/settings/dev.py
from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

# Local PostgreSQL (or sqlite if preferred)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "petuk_local_db"),
        "USER": os.getenv("DB_USER", "saponali"),
        "PASSWORD": os.getenv("DB_PASSWORD", "your_dev_password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Cookies (dev: no HTTPS)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# SSLCommerz sandbox
SSLCOMMERZ["issandbox"] = True
SSLCOMMERZ_VALIDATION_URL = "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"

# Optional dev tools
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
INTERNAL_IPS = ["127.0.0.1"]
