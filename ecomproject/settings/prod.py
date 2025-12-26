from .base import *
import os

DEBUG = False
SECRET_KEY = get_required("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = split_csv("ALLOWED_HOSTS", "petukhotel.com,www.petukhotel.com,petuk-hotel-django.onrender.com")
CSRF_TRUSTED_ORIGINS = split_csv("CSRF_TRUSTED_ORIGINS", "https://petukhotel.com,https://www.petukhotel.com,https://petuk-hotel-django.onrender.com")

# Database
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(
        default=get_required("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cloudinary (optional)
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")
if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# SSLCommerz (live)
SSLCOMMERZ = {
    "store_id": get_required("SSLC_STORE_ID"),
    "store_pass": get_required("SSLC_STORE_PASS"),
    "issandbox": get_bool("SSLC_ISSANDBOX", "False"),
}
SSLCOMMERZ_VALIDATION_URL = os.environ.get(
    "SSLC_VALIDATION_URL",
    "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php"
)


