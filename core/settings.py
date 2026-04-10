# --- FICHIERS STATIQUES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "hub" / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- CONFIGURATION CLOUDINARY (MEDIA) ---
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}

# L'URL média doit rester simple pour que Cloudinary prenne le relais
MEDIA_URL = '/media/'

# ON NE DÉFINIT PAS DE MEDIA_ROOT ICI ! (C'est supprimé)

# --- REDIRECTIONS ---
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