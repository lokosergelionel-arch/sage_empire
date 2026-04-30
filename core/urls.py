from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hub.views import (
    home, inscription_styliste, login_view, edit_profil, dashboard_styliste,
    mes_publications, supprimer_creation, galerie_mode, liste_stylistes,
    portfolio_styliste, page_immobilier, page_evenementiel, sage_digital,
    verify_email, renvoyer_email_verification,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
)

urlpatterns = [
    path('', home, name='home'),

    # ===================== PASSWORD RESET (Externes) =====================
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ===================== ADMIN =====================
    path('admin/', admin.site.urls),

    # ===================== AUTRES URLS =====================
    path('login/', login_view, name='login'),
    path('rejoindre/', inscription_styliste, name='inscription_styliste'),
    path('mon-espace/', dashboard_styliste, name='dashboard_styliste'),
    path('profil/modifier/', edit_profil, name='edit_profil'),
    path('mes-publications/', mes_publications, name='mes_publications'),
    path('supprimer-creation/<int:creation_id>/', supprimer_creation, name='supprimer_creation'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('verification-sent/', lambda r: render(r, 'verification_sent.html'), name='verification_sent'),
    path('renvoyer-verification/', renvoyer_email_verification, name='renvoyer_email_verification'),
    path('digital/', sage_digital, name='sage_digital'),
    path('immobilier/', page_immobilier, name='immobilier'),
    path('evenementiel/', page_evenementiel, name='evenementiel'),
    path('mode/', galerie_mode, name='galerie_mode'),
    path('marketplace/annuaire/', liste_stylistes, name='liste_stylistes'),
    path('styliste/<int:styliste_id>/', portfolio_styliste, name='portfolio_styliste'),

    # Django default auth (en dernier)
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)