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

from .forms import (
    InscriptionStylisteForm,
    EditProfilForm,
    CreationForm,
    PropertyForm,  # Nouveau
    PropertyAvailabilityForm  # Nouveau
)
from .models import (
    ProfilStyliste,
    Creation,
    Immobilier,
    Event,
    ProfilProprietaire,  # Nouveau
    Property,  # Nouveau
    PropertyMedia,  # Nouveau
    PropertyAvailability,  # Nouveau
    VisitRequest,  # Nouveau
    InvitationCode  # Nouveau
)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


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
    biens = Immobilier.objects.all()
    return render(request, 'immobilier.html', {'biens': biens})


def page_evenementiel(request):
    evenements = Event.objects.all().order_by('-date')
    return render(request, 'evenementiel.html', {'evenements': evenements})


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

            email_envoye = send_verification_email(request, user)
            if email_envoye:
                return redirect('verification_sent')
            else:
                return redirect('login')
    else:
        form = InscriptionStylisteForm()
    return render(request, 'inscription.html', {'form': form})


# ===================== MODIFIER PROFIL STYLISTE =====================
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

    return render(request, 'edit_profil.html', {
        'form': form,
        'styliste': styliste
    })


# ===================== DASHBOARD STYLISTE =====================
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
    return render(request, 'mes_publications.html', {
        'styliste': styliste,
        'creations': creations
    })


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
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            if hasattr(user, 'profil_proprietaire'):
                return redirect('dashboard_proprietaire')
            return redirect('dashboard_styliste')
        return render(request, 'registration/login.html', {'error': 'Identifiants invalides'})

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

    context = {
        'profil': profil,
        'properties': properties,
    }
    return render(request, 'proprietaire/mes_biens.html', context)


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

    context = {
        'form': form,
        'profil': profil,
    }
    return render(request, 'proprietaire/creer_bien.html', context)


@login_required
@proprietaire_required
def gestion_bien(request, property_id):
    profil = request.user.profil_proprietaire
    bien = get_object_or_404(Property, id=property_id, owner=profil)
    medias = bien.medias.all().order_by('order')
    availabilities = bien.availabilities.all()
    visit_requests = VisitRequest.objects.filter(property=bien).order_by('-created_at')

    context = {
        'profil': profil,
        'bien': bien,
        'medias': medias,
        'availabilities': availabilities,
        'visit_requests': visit_requests,
    }
    return render(request, 'proprietaire/gestion_bien.html', context)


@login_required
@proprietaire_required
def demandes_visite(request):
    profil = request.user.profil_proprietaire
    visites = VisitRequest.objects.filter(property__owner=profil).order_by('-created_at')

    context = {
        'profil': profil,
        'visites': visites,
    }
    return render(request, 'proprietaire/demandes_visite.html', context)


# ===================== INSCRIPTION PROPRIETAIRE =====================
def inscription_proprietaire(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            invitation = InvitationCode.objects.get(code=code, is_used=False)
            messages.success(request, "Code valide ! Veuillez compléter votre inscription.")
            return redirect('complete_inscription_proprietaire')
        except InvitationCode.DoesNotExist:
            messages.error(request, "Code d'invitation invalide ou déjà utilisé.")

    return render(request, 'proprietaire/inscription_proprietaire.html')


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
        send_mail(
            subject=subject,
            message=message,
            from_email='Sage Empire <loko.sergelionel@gmail.com>',
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"✅ Email de vérification envoyé à {user.email}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")
        return False


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        profil = user.profil
        profil.email_verifie = True
        profil.save()
        return render(request, 'email_verified_success.html')
    else:
        return render(request, 'email_verified_failed.html')


@login_required
def renvoyer_email_verification(request):
    user = request.user
    if user.email:
        email_envoye = send_verification_email(request, user)
        if email_envoye:
            return render(request, 'verification_sent.html', {'email_renvoye': True})
        else:
            return render(request, 'verification_sent.html', {'erreur': True})
    return redirect('edit_profil')


# ===================== PASSWORD RESET =====================
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/styliste_password_reset.html'
    email_template_name = 'registration/styliste_password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('styliste_password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/styliste_password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/styliste_password_reset_confirm.html'
    success_url = reverse_lazy('styliste_password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/styliste_password_reset_complete.html'