import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # vérifie si c'est 'core' ou 'sage_empire'
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    user.email = 'loko.sergelionel@gmail.com'
    # ON CHANGE LE MOT DE PASSE DIRECTEMENT ICI
    user.set_password('TonNouveauMdp2026!')
    user.save()
    print("SUCCÈS : Email mis à jour et Mot de passe réinitialisé en : TonNouveauMdp2026!")
except User.DoesNotExist:
    print("ERREUR : L'utilisateur admin n'existe pas.")