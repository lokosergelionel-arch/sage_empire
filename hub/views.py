from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.timezone import now

from .forms import (
    InscriptionStylisteForm,
    EditProfilForm,
    CreationForm,
    PropertyForm,
    PropertyAvailabilityForm,
    InvitationCodeForm,
    CompleteProprietaireForm,
)

from .models import (
    ProfilStyliste,
    Creation,
    Event,
    ProfilProprietaire,
    Property,
    PropertyMedia, # Ajouté si nécessaire
    PropertyAvailability,
    VisitRequest,
    InvitationCode
)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


# ===================== REDIRECTION INTELLIGENTE =====================
@login_required
def redirection_apres_login(request):
    """Redirige l'utilisateur vers son dashboard selon son profil"""
    try:
        if hasattr(request.user, 'profil_proprietaire'):
            return redirect('dashboard_proprietaire')
        elif hasattr(request.user, 'profil_styliste'):
            return redirect('dashboard_styliste')
        return redirect('home')
    except Exception:
        return redirect('home')


# ===================== DECORATEUR PROPRIETAIRE =====================
def proprietaire_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profil_proprietaire'):
            messages.warning(request, "Vous n'avez pas accès à cet espace.")
            return redirect('dashboard_styliste')
        return view_func(request, *args, **kwargs)
    return wrapper_func


# ===================== PAGES PUBLIQUES =====================
def home(request):
    creations = Creation.objects.all().order_by('-id')[:6]
    return render(request, 'index.html', {'creations': creations})


def page_immobilier(request):
    properties = Property.objects.filter(status='published', is_active=True).order_by('-date_creation')
    return render(request, 'immobilier.html', {'properties': properties})


def page_evenementiel(request):
    evenements = Event.objects.all().order_by('-date')
    return render(request, 'evenementiel.html', {'evenements': evenements})


def sage_digital(request):
    return render(request, 'sage_digital.html')


def verification_sent(request):
    return render(request, 'verification_sent.html')


# ===================== SAGE MODE =====================
def galerie_mode(request):
    try:
        profil_sage = ProfilStyliste.objects.get(user__username="sagemode_admin")
        produits = Creation.objects.filter(styliste=profil_sage).order_by('-id')
    except ProfilStyliste.DoesNotExist:
        produits = []
    return render(request, 'galerie_mode.html', {'produits_sage': produits})


def liste_stylistes(request):
    stylistes = ProfilStyliste.objects.exclude(user__username="sagemode_admin")
    return render(request, 'annuaire_stylistes.html', {'stylistes': stylistes})


def portfolio_styliste(request, styliste_id):
    styliste = get_object_or_404(ProfilStyliste, id=styliste_id)
    creations = Creation.objects.filter(styliste=styliste).order_by('-id')
    return render(request, 'portfolio_styliste.html', {
        'styliste': styliste,
        'creations': creations
    })


# ===================== INSCRIPTION STYLISTE =====================
def inscription_styliste(request):
    if request.method == 'POST':
        form = InscriptionStylisteForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profil = form.save(commit=False)
            profil.user = user
            profil.email_verifie = False
            profil.save()

            if send_verification_email(request, user):
                return redirect('verification_sent')
            return redirect('login')
    else:
        form = InscriptionStylisteForm()
    return render(request, 'inscription.html', {'form': form})


# ===================== PROFIL & DASHBOARD STYLISTE =====================
@login_required
def edit_profil(request):
    styliste = get_object_or_404(ProfilStyliste, user=request.user)
    if request.method == 'POST':
        form = EditProfilForm(request.POST, request.FILES, instance=styliste)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            if email and email != request.user.email:
                request.user.email = email
                request.user.save()
            return redirect('dashboard_styliste')
    else:
        form = EditProfilForm(instance=styliste, initial={'email': request.user.email})
    return render(request, 'edit_profil.html', {'form': form, 'styliste': styliste})


@login_required
def dashboard_styliste(request):
    styliste, _ = ProfilStyliste.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            creation = form.save(commit=False)
            creation.styliste = styliste
            creation.image_url = request.POST.get('image_url')
            creation.image_dos_url = request.POST.get('image_dos_url')
            creation.public_id = request.POST.get('public_id') or ""
            if request.POST.get('public_id_dos'):
                creation.public_id = f"{creation.public_id},{request.POST.get('public_id_dos')}".strip(',')
            creation.save()
            return redirect('dashboard_styliste')

    mes_creations = Creation.objects.filter(styliste=styliste).order_by('-id')
    return render(request, 'dashboard_styliste.html', {
        'styliste': styliste,
        'creations': mes_creations
    })


@login_required
def mes_publications(request):
    styliste = get_object_or_404(ProfilStyliste, user=request.user)
    creations = Creation.objects.filter(styliste=styliste).order_by('-id')
    return render(request, 'mes_publications.html', {'styliste': styliste, 'creations': creations})


@login_required
def supprimer_creation(request, creation_id):
    styliste = get_object_or_404(ProfilStyliste, user=request.user)
    creation = get_object_or_404(Creation, id=creation_id, styliste=styliste)
    if request.method == 'POST':
        creation.delete()
    return redirect('dashboard_styliste')


# ===================== LOGIN =====================
def login_view(request):
    if not User.objects.filter(username='sagemode_admin').exists():
        User.objects.create_superuser('sagemode_admin', 'admin@email.com', 'Empire2026!')

    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            # Utilisation de la redirection intelligente
            return redirect('redirect_user')
        messages.error(request, 'Identifiants invalides')
    return render(request, 'registration/login.html')


# ===================== ESPACE PROPRIETAIRE =====================
@login_required
@proprietaire_required
def dashboard_proprietaire(request):
    profil = request.user.profil_proprietaire
    properties = Property.objects.filter(owner=profil).order_by('-date_creation')
    visit_requests = VisitRequest.objects.filter(property__owner=profil).order_by('-created_at')[:5]

    context = {
        'profil': profil,
        'properties': properties,
        'visit_requests': visit_requests,
        'total_biens': properties.count(),
        'total_visites': visit_requests.count(),
    }
    return render(request, 'proprietaire/dashboard_proprietaire.html', context)


@login_required
@proprietaire_required
def mes_biens(request):
    profil = request.user.profil_proprietaire
    properties = Property.objects.filter(owner=profil).order_by('-date_creation')
    return render(request, 'proprietaire/mes_biens.html', {'profil': profil, 'properties': properties})


@login_required
@proprietaire_required
def creer_bien(request):
    profil = request.user.profil_proprietaire
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            bien = form.save(commit=False)
            bien.owner = profil
            bien.status = 'pending'
            bien.save()
            messages.success(request, "Votre bien a été créé avec succès et est en attente de validation.")
            return redirect('mes_biens')
    else:
        form = PropertyForm()
    return render(request, 'proprietaire/creer_bien.html', {'form': form, 'profil': profil})


@login_required
@proprietaire_required
def gestion_bien(request, property_id):
    profil = request.user.profil_proprietaire
    bien = get_object_or_404(Property, id=property_id, owner=profil)
    context = {
        'profil': profil,
        'bien': bien,
        'medias': bien.medias.all().order_by('order'),
        'availabilities': bien.availabilities.all(),
        'visit_requests': VisitRequest.objects.filter(property=bien).order_by('-created_at'),
    }
    return render(request, 'proprietaire/gestion_bien.html', context)


@login_required
@proprietaire_required
def demandes_visite(request):
    profil = request.user.profil_proprietaire
    visites = VisitRequest.objects.filter(property__owner=profil).order_by('-created_at')
    return render(request, 'proprietaire/demandes_visite.html', {'profil': profil, 'visites': visites})


# ===================== INSCRIPTION PROPRIETAIRE =====================
def inscription_proprietaire(request):
    if request.method == 'POST':
        form = InvitationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip().upper()
            try:
                InvitationCode.objects.get(code=code, is_used=False)
                request.session['invitation_code'] = code
                return redirect('complete_inscription_proprietaire')
            except InvitationCode.DoesNotExist:
                messages.error(request, "Ce code d'invitation est invalide ou déjà utilisé.")
    else:
        form = InvitationCodeForm()
    return render(request, 'proprietaire/inscription_proprietaire.html', {'form': form})


def complete_inscription_proprietaire(request):
    code = request.session.get('invitation_code')
    if not code:
        messages.error(request, "Session expirée. Veuillez recommencer.")
        return redirect('inscription_proprietaire')

    try:
        invitation = InvitationCode.objects.get(code=code, is_used=False)
    except InvitationCode.DoesNotExist:
        messages.error(request, "Code invalide.")
        return redirect('inscription_proprietaire')

    if request.method == 'POST':
        form = CompleteProprietaireForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['nom_complet'].lower().replace(" ", ""),
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profil = form.save(commit=False)
            profil.user = user
            profil.est_verifie = True
            profil.save()

            invitation.is_used = True
            invitation.proprietaire = profil
            invitation.used_at = now()
            invitation.save()

            login(request, user)
            messages.success(request, "Votre compte propriétaire a été créé avec succès !")
            return redirect('dashboard_proprietaire')
    else:
        form = CompleteProprietaireForm()
    return render(request, 'proprietaire/complete_inscription_proprietaire.html', {'form': form})


# ===================== EMAIL VERIFICATION =====================
def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'

    subject = "Confirmez votre adresse email - Sage Empire"
    message = render_to_string('email_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'protocol': protocol,
        'uid': uid,
        'token': token,
    })

    try:
        send_mail(subject, message, 'Sage Empire <loko.sergelionel@gmail.com>', [user.email], fail_silently=False)
        return True
    except Exception as e:
        print(f"Erreur email : {e}")
        return False


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        # Correction : on vérifie les deux types de profils possibles
        profil = getattr(user, 'profil_styliste', None) or getattr(user, 'profil_proprietaire', None)
        if profil:
            profil.email_verifie = True if hasattr(profil, 'email_verifie') else profil.est_verifie
            profil.save()
        return render(request, 'email_verified_success.html')
    return render(request, 'email_verified_failed.html')


@login_required
def renvoyer_email_verification(request):
    if send_verification_email(request, request.user):
        return render(request, 'verification_sent.html', {'email_renvoye': True})
    return redirect('edit_profil')


# ===================== PASSWORD RESET (NOMS SYNCHROS AVEC URLS.PY) =====================
class CustomPassword_reset_view(PasswordResetView):
    template_name = 'registration/styliste_password_reset.html'
    email_template_name = 'registration/styliste_password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('styliste_password_reset_done')


class CustomPassword_reset_done_view(PasswordResetDoneView):
    template_name = 'registration/styliste_password_reset_done.html'


class CustomPassword_reset_confirm_view(PasswordResetConfirmView):
    template_name = 'registration/styliste_password_reset_confirm.html'
    success_url = reverse_lazy('styliste_password_reset_complete')


class CustomPassword_reset_complete_view(PasswordResetCompleteView):
    template_name = 'registration/styliste_password_reset_complete.html'


# ===================== GESTION DU CALENDRIER =====================
@login_required
@proprietaire_required
def ajouter_disponibilite(request, property_id):
    bien = get_object_or_404(Property, id=property_id, owner=request.user.profil_proprietaire)
    if request.method == 'POST':
        form = PropertyAvailabilityForm(request.POST)
        if form.is_valid():
            disponibilite = form.save(commit=False)
            disponibilite.property = bien
            disponibilite.save()
            messages.success(request, "Période ajoutée avec succès.")
    return redirect('gestion_bien', property_id=bien.id)


@login_required
@proprietaire_required
def supprimer_disponibilite(request, disponibilite_id):
    disponibilite = get_object_or_404(PropertyAvailability, id=disponibilite_id)
    if disponibilite.property.owner == request.user.profil_proprietaire:
        bien_id = disponibilite.property.id
        disponibilite.delete()
        messages.success(request, "Période supprimée.")
        return redirect('gestion_bien', property_id=bien_id)
    return redirect('dashboard_proprietaire')