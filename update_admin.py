import os
import django

# FORCE LA CONFIGURATION
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def force_update():
    try:
        # On essaie de trouver l'admin par son pseudo
        user = User.objects.get(username='admin')
        user.email = 'loko.sergelionel@gmail.com'
        user.set_password('SageEmpire2026!') # NOTE BIEN CE MDP
        user.save()
        print("--- SAGE EMPIRE : ADMIN MIS À JOUR AVEC SUCCÈS ---")
    except User.DoesNotExist:
        # Si 'admin' n'existe pas, on le crée carrément
        User.objects.create_superuser('admin', 'loko.sergelionel@gmail.com', 'SageEmpire2026!')
        print("--- SAGE EMPIRE : NOUVEL ADMIN CRÉÉ AVEC SUCCÈS ---")

if __name__ == "__main__":
    force_update()