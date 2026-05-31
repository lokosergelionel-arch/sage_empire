from django.contrib import admin
from .models import (
    ProfilStyliste, Creation, Event,
    ProfilProprietaire, Property, PropertyMedia,
    PropertyAvailability, VisitRequest, InvitationCode
)

# --- ESPACE MODE & ÉVÉNEMENTS ---

@admin.register(ProfilStyliste)
class ProfilStylisteAdmin(admin.ModelAdmin):
    # Ajout de 'id' et 'email_verifie' modifiable directement pour aller plus vite
    list_display = ('id', 'nom_marque', 'user', 'email_verifie', 'date_inscription')
    list_editable = ('email_verifie',)
    search_fields = ('nom_marque', 'user__username', 'user__email')
    list_filter = ('email_verifie', 'date_inscription')

@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'styliste', 'prix', 'date_post')
    list_filter = ('styliste', 'date_post')
    search_fields = ('titre', 'styliste__nom_marque')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date')
    search_fields = ('titre',)


# --- ESPACE IMMOBILIER ---

@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'proprietaire', 'created_at', 'used_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('code', 'proprietaire__nom_complet')
    readonly_fields = ('code', 'created_at', 'used_at') # Évite de modifier un code par erreur

@admin.register(ProfilProprietaire)
class ProfilProprietaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_complet', 'user', 'est_verifie', 'date_inscription')
    list_editable = ('est_verifie',)
    search_fields = ('nom_complet', 'user__username', 'user__email')
    list_filter = ('est_verifie', 'date_inscription')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('titre', 'owner', 'type_bien', 'status', 'prix', 'is_active')
    list_editable = ('status', 'is_active') # Permet de publier/bloquer un bien en un clic
    list_filter = ('status', 'type_bien', 'is_active')
    search_fields = ('titre', 'quartier', 'owner__nom_complet')

# Amélioration de l'affichage des modèles secondaires
@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_video', 'order')
    list_filter = ('is_video', 'property')

@admin.register(PropertyAvailability)
class PropertyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date')
    list_filter = ('start_date', 'property')

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'nom_visiteur', 'telephone_visiteur', 'date_visite', 'created_at')
    list_filter = ('date_visite', 'created_at')
    search_fields = ('nom_visiteur', 'property__titre')