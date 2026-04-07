from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import ProfilStyliste, Creation, Immobilier, Event
from .forms import InscriptionStylisteForm


# --- 1. PAGES PUBLIQUES ---

def home(request):
    creations = Creation.objects.all().order_by('-id')[:6]
    return render(request, 'index.html', {'creations': creations})


def page_immobilier(request):
    biens = Immobilier.objects.all()
    return render(request, 'immobilier.html', {'biens': biens})


def page_evenementiel(request):
    evenements = Event.objects.all().order_by('-date')
    return render(request, 'evenementiel.html', {'evenements': evenements})


# --- 2. UNIVERS MODE & MARKETPLACE ---

def galerie_mode(request):
    # On cherche le profil de l'admin sagemode
    try:
        profil_sage = ProfilStyliste.objects.get(user__username="sagemode_admin")
        produits = Creation.objects.filter(styliste=profil_sage).order_by('-id')
    except ProfilStyliste.DoesNotExist:
        produits = []

    return render(request, 'galerie_mode.html', {'produits_sage': produits})


def liste_stylistes(request):
    """Annuaire des créateurs (on exclut l'admin de Sage Mode)"""
    stylistes = ProfilStyliste.objects.exclude(user__username="sagemode_admin")
    return render(request, 'annuaire_stylistes.html', {'stylistes': stylistes})


def portfolio_styliste(request, styliste_id):
    """Affiche le portfolio d'un styliste spécifique"""
    try:
        styliste = ProfilStyliste.objects.get(id=styliste_id)
        creations = Creation.objects.filter(styliste=styliste).order_by('-id')
    except ProfilStyliste.DoesNotExist:
        styliste = {"nom_marque": "Sage Empire", "biographie": "Bientôt disponible"}
        creations = []

    # J'ai enlevé 'hub/' devant car Django cherche déjà dans tes dossiers templates
    return render(request, 'portfolio_styliste.html', {
        'styliste': styliste,
        'creations': creations
    })


# --- 3. GESTION DES CRÉATEURS ---

def inscription_styliste(request):
    if request.method == 'POST':
        form = InscriptionStylisteForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            profil = form.save(commit=False)
            profil.user = user
            profil.save()
            return redirect('login')
    else:
        form = InscriptionStylisteForm()
    return render(request, 'inscription.html', {'form': form})


@login_required
def dashboard_styliste(request):
    """Espace privé pour ajouter/gérer ses créations"""
    styliste, created = ProfilStyliste.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        prix = request.POST.get('prix')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if titre and prix and image:
            Creation.objects.create(
                styliste=styliste,
                titre=titre,
                prix=prix,
                description=description,
                image=image
            )
            return redirect('dashboard_styliste')

    mes_creations = Creation.objects.filter(styliste=styliste).order_by('-id')
    return render(request, 'dashboard_styliste.html', {
        'styliste': styliste,
        'creations': mes_creations
    })


@login_required
def supprimer_creation(request, creation_id):
    styliste = get_object_or_404(ProfilStyliste, user=request.user)
    creation = get_object_or_404(Creation, id=creation_id, styliste=styliste)
    if request.method == 'POST':
        creation.delete()
    return redirect('dashboard_styliste')


# --- 4. CONNEXION & DIVERS ---

def login_view(request):
    # 1. Création automatique de sageempire_admin s'il n'existe pas
    if not User.objects.filter(username='sageempire_admin').exists():
        User.objects.create_superuser('sageempire_admin', 'admin@sageempire.com', 'S@ge2026!')

    # 2. Création automatique de sagemode_admin s'il n'existe pas
    if not User.objects.filter(username='sagemode_admin').exists():
        User.objects.create_superuser('sagemode_admin', 'admin@email.com', 'Empire2026!')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            return redirect('dashboard_styliste')
        else:
            return render(request, 'registration/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'registration/login.html')


def sage_digital(request):
    return render(request, 'sage_digital.html')