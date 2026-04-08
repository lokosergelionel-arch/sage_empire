from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <-- L'IMPORTATION CORRIGÉE ICI

from hub import views

urlpatterns = [
    # Administration
    path('admin/', admin.site.urls),
    path('digital/', views.sage_digital, name='sage_digital'),

    # Page d'accueil (Le Hub)
    path('', views.home, name='home'),

    # Inscription et Espace Styliste
    path('rejoindre/', views.inscription_styliste, name='inscription_styliste'),
    path('mon-espace/', views.dashboard_styliste, name='dashboard_styliste'),
    path('supprimer-creation/<int:creation_id>/', views.supprimer_creation, name='supprimer_creation'),

    # Services de l'Empire
    path('immobilier/', views.page_immobilier, name='immobilier'),
    path('evenementiel/', views.page_evenementiel, name='evenementiel'),

    # --- PARTIE MARKETPLACE ---
    path('mode/', views.galerie_mode, name='galerie_mode'),
    path('marketplace/annuaire/', views.liste_stylistes, name='liste_stylistes'),
    path('styliste/<int:styliste_id>/', views.portfolio_styliste, name='portfolio_styliste'),

    # Authentification
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    # Ajoute cette ligne pour inclure toutes les vues d'authentification (login, logout, password_reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Routes pour la réinitialisation du mot de passe (Utilisent auth_views importé plus haut)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

# CETTE LIGNE DOIT ÊTRE EXACTEMENT COMME ÇA :
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# GESTION DES IMAGES (Media) - Crucial pour voir les photos de profil
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)