
import environ
from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1','petukhotel.com', 'www.petukhotel.com', 'petuk-hotel-django.onrender.com']


CSRF_TRUSTED_ORIGINS = [
    'https://petukhotel.com',
    'https://www.petukhotel.com',
    'https://petuk-hotel-django.onrender.com',
]

SECURE_SSL_REDIRECT = True # যদি TLS certificate থাকে 
CSRF_COOKIE_SECURE = True 
SESSION_COOKIE_SECURE = True 
SESSION_COOKIE_SAMESITE = "None" # cross-site প্রয়োজন হলে

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'taggit',
    'django_ckeditor_5',
    'easyaudit',

    # Custom Apps
    'core',
    'userauths',
    'blog',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

ROOT_URLCONF = 'ecomproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'core.context_processor.core_context',
                'blog.context_processor.blog_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomproject.wsgi.application'


if env('DATABASE_URL', default=None):
    DATABASES = {
        'default': dj_database_url.config(
            default=env('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST', default='127.0.0.1'),
            'PORT': env('DB_PORT', default='5432'),
        }
    }




# DATABASES = {
#      'default': { 
#         'ENGINE': 'django.db.backends.postgresql', 
#         'NAME': env('DB_NAME'), 
#         'USER': env('DB_USER'), 
#         'PASSWORD': env('DB_PASSWORD'), 
#         'HOST': env('DB_HOST', default='127.0.0.1'), 
#         'PORT': env('DB_PORT', default='3306'), 
#         'CONN_MAX_AGE': 300, # persistent connections
#     } 
        
# }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = "/media/"
# Uncomment if you want local storage
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'uploads/'

SSLCOMMERZ = {
    'store_id': env('SSLC_STORE_ID'),
    'store_pass': env('SSLC_STORE_PASS'),
    'issandbox': env('SSLC_IS_SANDBOX'),  # False for production
    'validation_url': env('SSLC_VALIDATION_URL'), # ✅ এখানে পড়বেন
}

LANGUAGE_CODE = 'bn'
TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_header': "Ecommerce",
    'site_brand': "Petuk Hotel",
    'login_logo': "assets/img/logo.svg",
    'site_logo': "assets/img/favicon.ico",
    'copyright': "Petuk Hotel ltd",
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "Go to Website", "url": "core:index", "new_window": True},
    ],
}

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


