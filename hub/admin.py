from django.contrib import admin
from .models import ProfilStyliste, Creation, Immobilier, Event

# On enregistre les modèles pour qu'ils apparaissent dans l'admin
admin.site.register(ProfilStyliste)
admin.site.register(Creation)
admin.site.register(Immobilier)
admin.site.register(Event)