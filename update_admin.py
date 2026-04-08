import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # Vérifie si ton dossier s'appelle bien 'core'
django.setup()

from django.contrib.auth.models import User

# On cherche l'admin et on lui met l'email
try:
    user = User.objects.get(username='admin') # Remplace 'admin' par ton vrai pseudo si besoin
    user.email = 'loko.sergelionel@gmail.com'
    user.save()
    print("Succès : L'email de l'admin a été mis à jour.")
except User.DoesNotExist:
    print("Erreur : L'utilisateur admin n'existe pas.")