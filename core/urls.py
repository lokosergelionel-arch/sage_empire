from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hub import views  # Import global pour utiliser views.nom_de_la_fonction

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
]

# CETTE LIGNE DOIT ÊTRE EXACTEMENT COMME ÇA :
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# GESTION DES IMAGES (Media) - Crucial pour voir les photos de profil
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)