from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponsePermanentRedirect

def redirect_to_custom_domain(request):
    return HttpResponsePermanentRedirect('https://www.sage-empire.com' + request.get_full_path())

    # Redirection du sous-domaine Render vers le domaine principal
    path('', redirect_to_custom_domain, name='redirect_custom_domain'),
# Imports de tes vues
from hub.views import (
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
)

urlpatterns = [
    # ===================== AUTH & PASSWORD RESET =====================
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ===================== EMAIL VERIFICATION =====================
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('verification-sent/', lambda r: render(r, 'verification_sent.html'), name='verification_sent'),
    path('renvoyer-verification/', renvoyer_email_verification, name='renvoyer_email_verification'),

    # ===================== ADMIN & MAIN =====================
    path('admin/', admin.site.urls),
    path('digital/', sage_digital, name='sage_digital'),

    # ===================== PROFIL & DASHBOARD =====================
    path('profil/modifier/', edit_profil, name='edit_profil'),
    path('mon-espace/', dashboard_styliste, name='dashboard_styliste'),
    path('mes-publications/', mes_publications, name='mes_publications'),
    path('supprimer-creation/<int:creation_id>/', supprimer_creation, name='supprimer_creation'),

    # ===================== PAGES PUBLIQUES =====================
    path('', home, name='home'),
    path('rejoindre/', inscription_styliste, name='inscription_styliste'),
    path('login/', login_view, name='login'),
    path('immobilier/', page_immobilier, name='immobilier'),
    path('evenementiel/', page_evenementiel, name='evenementiel'),

    # ===================== SAGE MODE (MARKETPLACE) =====================
    path('mode/', galerie_mode, name='galerie_mode'),
    path('marketplace/annuaire/', liste_stylistes, name='liste_stylistes'),
    path('styliste/<int:styliste_id>/', portfolio_styliste, name='portfolio_styliste'),

    # Django Auth (optionnel)
    path('accounts/', include('django.contrib.auth.urls')),
]

# ===================== STATIC & MEDIA FILES =====================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)