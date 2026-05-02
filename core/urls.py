from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hub.views import (
    # === Vues existantes ===
    home,
    inscription_styliste,
    login_view,
    edit_profil,
    dashboard_styliste,
    mes_publications,
    supprimer_creation,
    galerie_mode,
    liste_stylistes,
    portfolio_styliste,
    page_immobilier,
    page_evenementiel,
    sage_digital,
    verify_email,
    renvoyer_email_verification,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,

    # === Vues Propriétaire ===
    dashboard_proprietaire,
    mes_biens,
    creer_bien,
    gestion_bien,
    demandes_visite,
    inscription_proprietaire,
)

urlpatterns = [
    path('', home, name='home'),

    # ===================== AUTHENTIFICATION =====================
    path('login/', login_view, name='login'),
    path('rejoindre/', inscription_styliste, name='inscription_styliste'),
    path('inscription-proprietaire/', inscription_proprietaire, name='inscription_proprietaire'),

    # Password Reset
    path('mot-de-passe-oublie/', CustomPasswordResetView.as_view(), name='styliste_password_reset'),
    path('mot-de-passe-oublie/done/', CustomPasswordResetDoneView.as_view(), name='styliste_password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='styliste_password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='styliste_password_reset_complete'),

    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('verification-sent/', lambda r: render(r, 'verification_sent.html'), name='verification_sent'),
    path('renvoyer-verification/', renvoyer_email_verification, name='renvoyer_email_verification'),

    # ===================== ESPACE STYLISTE =====================
    path('mon-espace/', dashboard_styliste, name='dashboard_styliste'),
    path('profil/modifier/', edit_profil, name='edit_profil'),
    path('mes-publications/', mes_publications, name='mes_publications'),
    path('supprimer-creation/<int:creation_id>/', supprimer_creation, name='supprimer_creation'),

    # ===================== PAGES PUBLIQUES =====================
    path('digital/', sage_digital, name='sage_digital'),
    path('immobilier/', page_immobilier, name='immobilier'),
    path('evenementiel/', page_evenementiel, name='evenementiel'),
    path('mode/', galerie_mode, name='galerie_mode'),
    path('marketplace/annuaire/', liste_stylistes, name='liste_stylistes'),
    path('styliste/<int:styliste_id>/', portfolio_styliste, name='portfolio_styliste'),

    # ===================== ESPACE PROPRIETAIRE =====================
    path('proprietaire/dashboard/', dashboard_proprietaire, name='dashboard_proprietaire'),
    path('proprietaire/mes-biens/', mes_biens, name='mes_biens'),
    path('proprietaire/creer-bien/', creer_bien, name='creer_bien'),
    path('proprietaire/bien/<int:property_id>/', gestion_bien, name='gestion_bien'),
    path('proprietaire/demandes-visite/', demandes_visite, name='demandes_visite'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)