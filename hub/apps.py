from django.apps import AppConfig
from django.db.models.signals import post_migrate

class HubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hub"

    def ready(self):
        post_migrate.connect(create_or_update_admin, sender=self)


def create_or_update_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    # On importe les signaux pour pouvoir les bloquer temporairement
    from django.db.models.signals import post_save

    username = 'admin'
    email = 'loko.sergelionel@gmail.com'
    password = 'SageEmpire2026!'

    # On vérifie si l'admin existe déjà
    user_exists = User.objects.filter(username=username).exists()

    if not user_exists:
        # On crée le superuser
        User.objects.create_superuser(username, email, password)
        print("--- SAGE EMPIRE : SUPERUSER CRÉÉ ---")
    else:
        # On met à jour l'admin existant
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.save()
        print("--- SAGE EMPIRE : ADMIN MIS À JOUR ---")