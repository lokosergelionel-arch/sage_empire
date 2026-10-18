import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ===================== SÉCURITÉ =====================
# NOTE : la valeur par défaut ci-dessous est publique (dans git). Définir SECRET_KEY
# dans les variables d'environnement Render. Pas d'erreur levée volontairement
# pour ne pas casser un déploiement si la variable est absente.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!-8t*1$y7g#epu8zj&)@=14q&$e+b%f(zuko_bsno^bm$k*$7_')

# Render définit RENDER=true : aucune variable à configurer pour la prod.
IS_PROD = bool(os.environ.get('RENDER'))
# DEBUG : True en local, False sur Render ; surcharge possible via env DEBUG ('1'/'0').
_debug_env = os.environ.get('DEBUG')
if _debug_env in ('1', '0'):
    DEBUG = _debug_env == '1'
else:
    DEBUG = not IS_PROD

ALLOWED_HOSTS = [
    'sage-empire.com',
    'www.sage-empire.com',
    'sage-empire.onrender.com',
    'localhost',
    '127.0.0.1'
]

CSRF_TRUSTED_ORIGINS = [
    'https://sage-empire.com',
    'https://www.sage-empire.com',
    'https://sage-empire.onrender.com'
]

# Sécurité HTTPS : actif uniquement hors DEBUG (production), désactivé en dev.
USE_X_FORWARDED_HOST = True
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
else:
    SECURE_PROXY_SSL_HEADER = None
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ===================== APPLICATIONS =====================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    "cloudinary_storage",
    "cloudinary",
    "hub",
]

# ===================== MIDDLEWARE =====================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "hub.middleware.CanonicalHostMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# SEO : domaine canonique
SITE_URL = "https://www.sage-empire.com"
WSGI_APPLICATION = "core.wsgi.application"

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
                "hub.context_processors.site_info",
            ],
        },
    },
]

# ===================== BASE DE DONNÉES =====================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )
} if os.environ.get('DATABASE_URL') else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===================== STATIC & MEDIA =====================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "hub" / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = "https://res.cloudinary.com/"

# STORAGES (Django >= 4.2) remplace STATICFILES_STORAGE / DEFAULT_FILE_STORAGE (supprimés en 5.1).
STORAGES = {
    'default': {'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    # Sans PREFIX, la lib utilise MEDIA_URL (URL absolue) comme préfixe de nom -> noms/URLs mal formés.
    'PREFIX': '',
}

# ===================== EMAIL (BREVO) =====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'Sage Empire <noreply@sage-empire.com>'
SERVER_EMAIL = 'noreply@sage-empire.com'

# ===================== AUTRES =====================
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# CORRECTION ICI : Redirection alignée sur le nom de la vue dans urls.py
LOGIN_REDIRECT_URL = 'redirection_apres_login'
LOGOUT_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===================== LOGGING (pour debug email) =====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
