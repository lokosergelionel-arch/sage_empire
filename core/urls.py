from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponsePermanentRedirect

from hub.views import (
    home, inscription_styliste, login_view, edit_profil, dashboard_styliste,
    mes_publications, supprimer_creation, galerie_mode, liste_stylistes,
    portfolio_styliste, page_immobilier, page_evenementiel, sage_digital,
    verify_email, renvoyer_email_verification, CustomPasswordResetView,
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)


def redirect_to_custom_domain(request):
    return HttpResponsePermanentRedirect('https://www.sage-empire.com' + request.get_full_path())


urlpatterns = [
    # ===================== REDIRECTION DOMAINE =====================
    path('', redirect_to_custom_domain, name='redirect_custom_domain'),

    # ===================== ADMIN (Style Django sombre) =====================
    path('admin/', admin.site.urls),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='admin/password_reset.html'
    ), name='admin_password_reset'),

    # ===================== PASSWORD RESET EXTERNES (Design Sage Empire) =====================
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

    # Django Auth URLs (on le garde en dernier pour ne pas écraser nos URLs personnalisées)
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)