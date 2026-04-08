import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SÉCURITÉ ---
# Garde ta clé actuelle pour le moment, mais sur Render tu pourras la cacher
SECRET_KEY = "django-insecure-!-8t*1$y7g#epu8zj&)@=14q&$e+b%f(zuko_bsno^bm$k*$7_"

# DEBUG reste True pour tes tests, on le passera à False pour le lancement final
DEBUG = True

# On autorise Render et ton ordi local
ALLOWED_HOSTS = ['sage-empire.onrender.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://sage-empire.onrender.com']
# --- APPLICATIONS ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "hub",
]

# --- MIDDLEWARE (L'ordre est CRUCIAL ici pour WhiteNoise) ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Gère tes images/CSS sur Render
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
        "DIRS": [BASE_DIR / 'templates'],  # Pour tes futurs fichiers HTML globaux
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
# SQLite est parfait pour tes tests avec l'équipe
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- VALIDATION MOTS DE PASSE ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- INTERNATIONALISATION ---
LANGUAGE_CODE = "fr-fr"  # Passé en Français pour l'Empire
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- FICHIERS STATIQUES (CSS, JS, IMAGES) ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "hub" / "static"]

# Dossier où Render va stocker les fichiers compilés
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Utilisation de WhiteNoise pour servir les fichiers statiques de manière ultra-rapide
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- REDIRECTIONS ---
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuration E-mail (Exemple avec Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'loko.sergelionel@gmail.com' # Ton adresse Gmail
EMAIL_HOST_PASSWORD = 'ppesinbmtjzuajak' # Code à 16 lettres généré par Google
DEFAULT_FROM_EMAIL = 'Sage Empire <loko.sergelionel@gmail.com>'
EMAIL_USE_SSL = False  # On utilise TLS (587), donc SSL doit être à False