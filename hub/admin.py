from django.contrib import admin
from django.utils import timezone  # Ajouté pour corriger le crash de l'action de groupe
from .models import (
    ProfilStyliste, Creation, Event,
    ProfilProprietaire, Property, PropertyMedia,
    PropertyAvailability, VisitRequest, InvitationCode
)

# ==============================================================================
#                      CHARTE GRAPHIQUE & TITRES SAGE EMPIRE
# ==============================================================================

# Personnalisation des titres textuels de l'interface d'administration
admin.site.site_header = "SAGE EMPIRE | Panel Technique"
admin.site.site_title = "Administration Sage Empire"
admin.site.index_title = "Gestion de l'Écosystème"

# Injection de la feuille de style CSS pour le look luxe (Anthracite & Or #B5935E)
admin.site.site_url = '/'  # Lien "Voir le site" renvoie à la racine publique
admin.site.enable_nav_sidebar = True


class EmpireAdminTheme:
    """Feuille de style injectée pour surcharger le thème par défaut de Django"""

    class Media:
        css = {
            'all': ('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap',)
        }
        # Injection dynamique directe des couleurs de l'Empire
        admin.site.site_header = admin.site.site_header


# Surcharge globale légère via CSS natif (optionnelle mais robuste)
# Note : Pour les versions récentes de Django, cela applique les variables CSS CSS.
admin.ModelAdmin.Media.css = {
    'all': ('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap',)
}


# ==============================================================================
#                         --- ESPACE MODE & ÉVÉNEMENTS ---
# ==============================================================================

@admin.register(ProfilStyliste)
class ProfilStylisteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_marque', 'user', 'email_verifie', 'date_inscription')
    list_editable = ('email_verifie',)
    search_fields = ('nom_marque', 'user__username', 'user__email')
    list_filter = ('email_verifie', 'date_inscription')

    # Bloque l'ajout direct par l'admin technique pour respecter les profils applicatifs
    def has_add_permission(self, request):
        return not request.user.is_superuser


@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'styliste', 'prix', 'disponible', 'date_post')
    list_filter = ('styliste', 'date_post', 'disponible')
    search_fields = ('titre', 'styliste__nom_marque')
    list_editable = ('disponible', 'prix')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date')
    search_fields = ('titre',)
    date_hierarchy = 'date'


# ==============================================================================
#                            --- ESPACE IMMOBILIER ---
# ==============================================================================

@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'proprietaire', 'created_at', 'used_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('code', 'proprietaire__nom_complet')
    readonly_fields = ('code', 'created_at', 'used_at')
    actions = ['mark_as_used']

    def mark_as_used(self, request, queryset):
        # Utilisation de timezone.now() pour éviter les erreurs d'exécution
        queryset.update(is_used=True, used_at=timezone.now())

    mark_as_used.short_description = "Marquer les codes comme utilisés"


@admin.register(ProfilProprietaire)
class ProfilProprietaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_complet', 'user', 'est_verifie', 'date_inscription')
    list_editable = ('est_verifie',)
    search_fields = ('nom_complet', 'user__username', 'user__email')
    list_filter = ('est_verifie', 'date_inscription')

    def has_add_permission(self, request):
        return not request.user.is_superuser


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('titre', 'owner', 'type_bien', 'status', 'prix', 'is_active', 'quartier')
    list_editable = ('status', 'is_active', 'prix')
    list_filter = ('status', 'type_bien', 'is_active', 'quartier')
    search_fields = ('titre', 'quartier', 'owner__nom_complet')


@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_video', 'order', 'validated')
    list_filter = ('is_video', 'property', 'validated')
    list_editable = ('order', 'validated')


@admin.register(PropertyAvailability)
class PropertyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'is_available')
    list_filter = ('start_date', 'property', 'is_available')
    list_editable = ('is_available',)
    date_hierarchy = 'start_date'


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'visitor_name',
        'visitor_phone',
        'requested_date',
        'status',
        'amount',
        'created_at'
    )
    list_filter = ('requested_date', 'status', 'created_at')
    search_fields = ('visitor_name', 'visitor_phone', 'property__titre')
    list_editable = ('status',)
    date_hierarchy = 'requested_date'