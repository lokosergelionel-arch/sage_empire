from django.contrib import admin
from .models import (
    ProfilStyliste, Creation, Event,
    ProfilProprietaire, Property, PropertyMedia,
    PropertyAvailability, VisitRequest, InvitationCode
)

# --- ESPACE MODE & ÉVÉNEMENTS ---

@admin.register(ProfilStyliste)
class ProfilStylisteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_marque', 'user', 'email_verifie', 'date_inscription')
    list_editable = ('email_verifie',)
    search_fields = ('nom_marque', 'user__username', 'user__email')
    list_filter = ('email_verifie', 'date_inscription')
    # Ajout pour éviter la création via admin (complémentaire aux validations dans models.py)
    def has_add_permission(self, request):
        return not request.user.is_superuser  # Bloque l'ajout par l'admin

@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'styliste', 'prix', 'disponible', 'date_post')  # Ajout de 'disponible'
    list_filter = ('styliste', 'date_post', 'disponible')
    search_fields = ('titre', 'styliste__nom_marque')
    list_editable = ('disponible', 'prix')  # Permet de modifier rapidement

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date')
    search_fields = ('titre',)
    date_hierarchy = 'date'  # Ajout d'un filtre par date hiérarchique

# --- ESPACE IMMOBILIER ---

@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'proprietaire', 'created_at', 'used_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('code', 'proprietaire__nom_complet')
    readonly_fields = ('code', 'created_at', 'used_at')
    # Action personnalisée pour marquer comme utilisé
    actions = ['mark_as_used']

    def mark_as_used(self, request, queryset):
        queryset.update(is_used=True, used_at=now())
    mark_as_used.short_description = "Marquer les codes comme utilisés"

@admin.register(ProfilProprietaire)
class ProfilProprietaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_complet', 'user', 'est_verifie', 'date_inscription')
    list_editable = ('est_verifie',)
    search_fields = ('nom_complet', 'user__username', 'user__email')
    list_filter = ('est_verifie', 'date_inscription')
    # Bloque aussi la création via admin pour les propriétaires
    def has_add_permission(self, request):
        return not request.user.is_superuser

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('titre', 'owner', 'type_bien', 'status', 'prix', 'is_active', 'quartier')
    list_editable = ('status', 'is_active', 'prix')
    list_filter = ('status', 'type_bien', 'is_active', 'quartier')
    search_fields = ('titre', 'quartier', 'owner__nom_complet')
    prepopulated_fields = {'titre': ('quartier',)}  # Suggestion auto pour le titre

@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_video', 'order', 'validated')
    list_filter = ('is_video', 'property', 'validated')
    list_editable = ('order', 'validated')  # Permet de réorganiser les médias

@admin.register(PropertyAvailability)
class PropertyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'is_available')
    list_filter = ('start_date', 'property', 'is_available')
    list_editable = ('is_available',)
    date_hierarchy = 'start_date'

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    # CORRECTION : Noms des champs alignés sur le modèle
    list_display = (
        'property',
        'visitor_name',  # Corrigé (ancien: 'nom_visiteur')
        'visitor_phone',  # Corrigé (ancien: 'telephone_visiteur')
        'requested_date',  # Corrigé (ancien: 'date_visite')
        'status',
        'amount',
        'created_at'
    )
    list_filter = ('requested_date', 'status', 'created_at')  # Corrigé
    search_fields = ('visitor_name', 'visitor_phone', 'property__titre')  # Corrigé
    list_editable = ('status',)  # Permet de mettre à jour le statut rapidement
    date_hierarchy = 'requested_date'  # Filtre par date pratique