from django.contrib import admin
from .models import (
    ProfilStyliste, Creation, Event,
    ProfilProprietaire, Property, PropertyMedia,
    PropertyAvailability, VisitRequest, InvitationCode
)

# --- ESPACE MODE & ÉVÉNEMENTS ---

@admin.register(ProfilStyliste)
class ProfilStylisteAdmin(admin.ModelAdmin):
    list_display = ('nom_marque', 'user', 'email_verifie', 'date_inscription')
    search_fields = ('nom_marque', 'user__username')

@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'styliste', 'prix', 'date_post')
    list_filter = ('styliste', 'date_post')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date')


# --- ESPACE IMMOBILIER (C'est ici que tu génères tes codes) ---

@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    # Ce qui s'affiche dans la liste
    list_display = ('code', 'is_used', 'proprietaire', 'created_at')
    # Filtre sur le côté pour voir qui a déjà utilisé son code
    list_filter = ('is_used',)
    # Barre de recherche pour retrouver un code précis
    search_fields = ('code',)

@admin.register(ProfilProprietaire)
class ProfilProprietaireAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'user', 'est_verifie', 'date_inscription')
    list_editable = ('est_verifie',) # Tu peux valider un proprio direct dans la liste

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('titre', 'owner', 'type_bien', 'status', 'prix')
    list_filter = ('status', 'type_bien')
    search_fields = ('titre', 'quartier')

# On enregistre le reste pour la forme
admin.site.register(PropertyMedia)
admin.site.register(PropertyAvailability)
admin.site.register(VisitRequest)