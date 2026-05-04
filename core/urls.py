from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# On importe tout directement depuis hub.views pour éviter les conflits
from hub.views import (
    home, inscription_styliste, login_view, edit_profil, dashboard_styliste,
    mes_publications, supprimer_creation, galerie_mode, liste_stylistes,
    portfolio_styliste, page_immobilier, page_evenementiel, sage_digital,
    verify_email, renvoyer_email_verification, verification_sent,
    CustomPassword_reset_view, CustomPassword_reset_done_view,
    CustomPassword_reset_confirm_view, CustomPassword_reset_complete_view,

    # La nouvelle vue de tri
    redirection_apres_login,

    # Vues Propriétaire
    dashboard_proprietaire, mes_biens, creer_bien, gestion_bien,
    demandes_visite, inscription_proprietaire, complete_inscription_proprietaire,
    ajouter_disponibilite, supprimer_disponibilite,
)

urlpatterns = [
    path('', home, name='home'),

    # Route de redirection intelligente après connexion
    path('redirect-user/', redirection_apres_login, name='redirect_user'),

    # Authentification
    path('login/', login_view, name='login'),
    path('rejoindre/', inscription_styliste, name='inscription_styliste'),
    path('inscription-proprietaire/', inscription_proprietaire, name='inscription_proprietaire'),
    path('complete-inscription/', complete_inscription_proprietaire, name='complete_inscription_proprietaire'),

    # Password Reset
    path('mot-de-passe-oublie/', CustomPassword_reset_view.as_view(), name='styliste_password_reset'),
    path('mot-de-passe-oublie/done/', CustomPassword_reset_done_view.as_view(), name='styliste_password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPassword_reset_confirm_view.as_view(),
         name='styliste_password_reset_confirm'),
    path('reset/done/', CustomPassword_reset_complete_view.as_view(), name='styliste_password_reset_complete'),

    # Email Verification
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('verification-sent/', verification_sent, name='verification_sent'),
    path('renvoyer-verification/', renvoyer_email_verification, name='renvoyer_email_verification'),

    # Espace Styliste
    path('mon-espace/', dashboard_styliste, name='dashboard_styliste'),
    path('profil/modifier/', edit_profil, name='edit_profil'),
    path('mes-publications/', mes_publications, name='mes_publications'),
    path('supprimer-creation/<int:creation_id>/', supprimer_creation, name='supprimer_creation'),

    # Pages Publiques
    path('digital/', sage_digital, name='sage_digital'),
    path('immobilier/', page_immobilier, name='immobilier'),
    path('evenementiel/', page_evenementiel, name='evenementiel'),
    path('mode/', galerie_mode, name='galerie_mode'),
    path('marketplace/annuaire/', liste_stylistes, name='liste_stylistes'),
    path('styliste/<int:styliste_id>/', portfolio_styliste, name='portfolio_styliste'),

    # Espace Propriétaire
    path('proprietaire/dashboard/', dashboard_proprietaire, name='dashboard_proprietaire'),
    path('proprietaire/mes-biens/', mes_biens, name='mes_biens'),
    path('proprietaire/creer-bien/', creer_bien, name='creer_bien'),
    path('proprietaire/bien/<int:property_id>/', gestion_bien, name='gestion_bien'),
    path('proprietaire/demandes-visite/', demandes_visite, name='demandes_visite'),

    # Gestion du calendrier
    path('proprietaire/bien/<int:property_id>/ajouter-disponibilite/',
         ajouter_disponibilite, name='ajouter_disponibilite'),
    path('proprietaire/supprimer-disponibilite/<int:disponibilite_id>/',
         supprimer_disponibilite, name='supprimer_disponibilite'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)