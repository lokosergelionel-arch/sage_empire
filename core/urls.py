from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponsePermanentRedirect

from hub.views import (
    home, inscription_styliste, login_view, edit_profil, dashboard_styliste,
    mes_publications, supprimer_creation, galerie_mode, liste_stylistes,
    portfolio_styliste, page_immobilier, page_evenementiel, sage_digital,
    verify_email, renvoyer_email_verification,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
)


# Redirect seulement si on est sur le mauvais domaine (ex: render subdomain)
def redirect_to_custom_domain(request):
    host = request.get_host()
    if host in ['sage-empire.onrender.com', 'sage-empire.render.com']:
        return HttpResponsePermanentRedirect('https://www.sage-empire.com' + request.get_full_path())
    return None


urlpatterns = [
    # ===================== HOME =====================
    path('', home, name='home'),

    # ===================== REDIRECTION (conditionnelle) =====================
    path('redirect/', lambda r: redirect('home'), name='redirect_custom_domain'),

    # ===================== ADMIN =====================
    path('admin/', admin.site.urls),

    # ===================== PASSWORD RESET EXTERNES =====================
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ===================== EMAIL VERIFICATION =====================
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('verification-sent/', lambda r: render(r, 'verification_sent.html'), name='verification_sent'),
    path('renvoyer-verification/', renvoyer_email_verification, name='renvoyer_email_verification'),

    # ===================== AUTRES PAGES =====================
    path('digital/', sage_digital, name='sage_digital'),
    path('profil/modifier/', edit_profil, name='edit_profil'),
    path('mon-espace/', dashboard_styliste, name='dashboard_styliste'),
    path('mes-publications/', mes_publications, name='mes_publications'),
    path('supprimer-creation/<int:creation_id>/', supprimer_creation, name='supprimer_creation'),
    path('rejoindre/', inscription_styliste, name='inscription_styliste'),
    path('login/', login_view, name='login'),
    path('immobilier/', page_immobilier, name='immobilier'),
    path('evenementiel/', page_evenementiel, name='evenementiel'),
    path('mode/', galerie_mode, name='galerie_mode'),
    path('marketplace/annuaire/', liste_stylistes, name='liste_stylistes'),
    path('styliste/<int:styliste_id>/', portfolio_styliste, name='portfolio_styliste'),

    # Django auth (en dernier)
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)