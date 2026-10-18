import os

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class HubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hub"

    def ready(self):
        post_migrate.connect(create_or_update_admin, sender=self)


def create_or_update_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    from django.db.models.signals import post_save

    username = 'admin'
    email = 'loko.sergelionel@gmail.com'
    # Le mot de passe vient de l'environnement (jamais écrit dans le code).
    password = os.environ.get('ADMIN_PASSWORD')
    reset_password = os.environ.get('ADMIN_RESET_PASSWORD') == '1'

    if not password:
        print("--- SAGE EMPIRE : ADMIN_PASSWORD absent, compte admin non modifié ---")
        return

    # --- MÉTHODE RADICALE : On bloque tous les signaux post_save temporairement ---
    receivers = post_save.receivers
    post_save.receivers = []

    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print("--- SAGE EMPIRE : SUPERUSER CRÉÉ ---")
        else:
            user = User.objects.get(username=username)
            user.email = email
            # Le mot de passe n'est remplacé que sur demande explicite.
            if reset_password:
                user.set_password(password)
            user.save()
            print("--- SAGE EMPIRE : ADMIN MIS À JOUR ---")
    finally:
        # On rétablit les signaux après l'opération
        post_save.receivers = receivers