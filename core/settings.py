import os
from pathlib import Path
import dj_database_url

# 1. BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SÉCURITÉ ---
SECRET_KEY = "django-insecure-!-8t*1$y7g#epu8zj&)@=14q&$e+b%f(zuko_bsno^bm$k*$7_"
DEBUG = True
ALLOWED_HOSTS = ['sage-empire.onrender.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://sage-empire.onrender.com']

# --- APPLICATIONS ---
INSTALLED_APPS = [
    "cloudinary_storage",  # OBLIGATOIRE EN PREMIER
    "django.contrib.staticfiles",
    "cloudinary",
    "hub",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# --- BASE DE DONNÉES ---
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=True if os.environ.get('DATABASE_URL') else False
    )
}

# --- INTERNATIONALISATION ---
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- FICHIERS STATIQUES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "hub" / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- CLOUDINARY (LÀ OÙ TOUT SE JOUE) ---
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ON FORCE LE STOCKAGE EXTERNE
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}

# L'URL devient un simple préfixe, Cloudinary gérera le reste
MEDIA_URL = '/media/'

# --- ATTENTION : AUCUNE LIGNE MEDIA_ROOT ICI ---

# --- REDIRECTIONS & AUTOFIELD ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CONFIGURATION EMAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'loko.sergelionel@gmail.com'
EMAIL_HOST_PASSWORD = 'ppesinbmtjzuajak'
DEFAULT_FROM_EMAIL = 'Sage Empire <loko.sergelionel@gmail.com>'