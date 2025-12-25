# ecomproject/settings/prod.py
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ["petukhotel.com", "www.petukhotel.com"]
CSRF_TRUSTED_ORIGINS = [
    "https://petukhotel.com",
    "https://www.petukhotel.com",
]

# Security
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"  # cross-site return দরকার হলে
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Production DB (Render/Cloud)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Emails (optional)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.sendgrid.net")
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@petukhotel.com")

# SSLCommerz live
SSLCOMMERZ["issandbox"] = False
SSLCOMMERZ_VALIDATION_URL = "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php"

# Logging: more detail in prod
LOGGING["root"]["level"] = "WARNING"
LOGGING["loggers"] = {
    "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    "payments": {"handlers": ["console"], "level": "INFO", "propagate": False},
}
