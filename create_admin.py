import os
import django

# Configure l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# TES IDENTIFIANTS SAGE EMPIRE
username = "sagemode_admin"
email = "admin@sage-empire.com"  # Modifié ici
password = "Empire2026!" # N'oublie pas de mettre ton vrai mot de passe ici

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser '{username}' créé avec succès !")
else:
    # Force la mise à jour du mot de passe pour garantir l'accès
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"ℹ️ L'utilisateur '{username}' existait déjà, mot de passe mis à jour.")