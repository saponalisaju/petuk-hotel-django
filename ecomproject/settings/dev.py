from .base import * 
import environ 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent.parent 

env = environ.Env() 
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env.bool("DEBUG", default=True) 
SECRET_KEY = env("DJANGO_SECRET_KEY", default="unsafe-dev-key")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

# Database (Postgres for dev)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

# Security flags relaxed for dev
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_SCHEME = env("SITE_SCHEME", default="http")
SITE_DOMAIN = env("SITE_DOMAIN", default="127.0.0.1:8000")

# Cloudinary (dev uploads)
CLOUDINARY_CLOUD_NAME = env("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY", default="")
CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET", default="")
if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# SSLCommerz (sandbox mode)
SSLCOMMERZ = {
    "store_id": env("SSLC_STORE_ID", default=""),
    "store_pass": env("SSLC_STORE_PASS", default=""),
    "issandbox": env.bool("SSLC_IS_SANDBOX", default=True),
}
SSLCOMMERZ_VALIDATION_URL = env(
    "SSLC_VALIDATION_URL",
    default="https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"
)
