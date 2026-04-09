import os
import django

# Configure l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
# On importe le modèle Profil pour éviter les erreurs
try:
    from hub.models import ProfilStyliste
except ImportError:
    ProfilStyliste = None

# TES IDENTIFIANTS SAGE EMPIRE
username = "sagemode_admin"
email = "admin@sage-empire.com"
password = "Empire2026!" # <--- METS TON VRAI PASS ICI

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superuser '{username}' créé !")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"ℹ️ Superuser '{username}' mis à jour.")
except Exception as e:
    print(f"⚠️ Erreur lors de la création de l'admin : {e}")