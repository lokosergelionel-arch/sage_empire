import os


from pathlib import Path

import dj_database_url

import cloudinary

import cloudinary.uploader

import cloudinary.api



BASE_DIR = Path(__file__).resolve().parent.parent



# ====================== SÉCURITÉ ======================

SECRET_KEY = "django-insecure-!-8t*1$y7g#epu8zj&)@=14q&$e+b%f(zuko_bsno^bm$k*$7_"

DEBUG = True

ALLOWED_HOSTS = ['sage-empire.onrender.com', 'sage-empire.com', 'www.sage-empire.com', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://sage-empire.onrender.com']



# ====================== APPLICATIONS ======================

INSTALLED_APPS = [

"django.contrib.admin",

"django.contrib.auth",

"django.contrib.contenttypes",

"django.contrib.sessions",

"django.contrib.messages",

"django.contrib.staticfiles",



"cloudinary_storage",

"cloudinary",

"hub",

]



# ====================== MIDDLEWARE ======================

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

],

},

},

]



# ====================== BASE DE DONNÉES ======================
import dj_database_url
import os

# Configuration qui marche à la fois en local et sur Render
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    # Base de données locale (SQLite) quand on est en développement
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ====================== STATIC & MEDIA ======================

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / "hub" / "static"]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



MEDIA_URL = "https://res.cloudinary.com/"



DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



CLOUDINARY_STORAGE = {

'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),

'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),

'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),

'SECURE': True,

}



# ====================== AUTRES ======================

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



LOGIN_REDIRECT_URL = 'dashboard_styliste'
LOGOUT_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




# ===================== EMAIL CONFIGURATION (BREVO) =====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30

# Identifiants Brevo
EMAIL_HOST_USER = 'a9b395001@smtp-brevo.com'
EMAIL_HOST_PASSWORD = 'U3phWGgtywIP2KqZ'

DEFAULT_FROM_EMAIL = 'loko.sergelionel@gmail.com'
SERVER_EMAIL = 'loko.sergelionel@gmail.com'

print("=== EMAIL BREVO CONFIGURÉ AVEC SUCCÈS ===")