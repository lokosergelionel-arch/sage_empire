from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login  # <--- AJOUTÉ POUR LA CONNEXION
from .models import ProfilStyliste, Creation, Immobilier, Event
from .forms import InscriptionStylisteForm


# --- 1. PAGES PUBLIQUES (ACCUEIL & HUB) ---

def home(request):
    """Page d'accueil principale avec la section Marketplace"""
    stylistes = ProfilStyliste.objects.all()
    return render(request, 'index.html', {'stylistes': stylistes})


def page_immobilier(request):
    """Page vitrine pour l'immobilier"""
    biens = Immobilier.objects.all()
    return render(request, 'immobilier.html', {'biens': biens})


def page_evenementiel(request):
    """Page vitrine pour l'événementiel"""
    evenements = Event.objects.all().order_by('-date')
    return render(request, 'evenementiel.html', {'evenements': evenements})


# --- 2. UNIVERS MODE & MARKETPLACE ---

def galerie_mode(request):
    """Affiche uniquement les créations de la marque SAGE MODE"""
    try:
        profil_sage = ProfilStyliste.objects.get(nom_marque="SAGE MODE")
        produits = Creation.objects.filter(styliste=profil_sage).order_by('-id')
    except ProfilStyliste.DoesNotExist:
        produits = []

    return render(request, 'galerie_mode.html', {'produits_sage': produits})


def liste_stylistes(request):
    """Annuaire des créateurs partenaires"""
    stylistes = ProfilStyliste.objects.exclude(nom_marque="SAGE MODE")
    return render(request, 'annuaire_stylistes.html', {'stylistes': stylistes})


def portfolio_styliste(request, styliste_id):
    """Portfolio individuel d'un styliste"""
    styliste = get_object_or_404(ProfilStyliste, id=styliste_id)
    oeuvres = Creation.objects.filter(styliste=styliste).order_by('-id')
    return render(request, 'portfolio_styliste.html', {
        'styliste': styliste,
        'oeuvres': oeuvres
    })


# --- 3. GESTION DES CRÉATEURS ---

def inscription_styliste(request):
    """Formulaire d'inscription pour les nouveaux partenaires"""
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
            return redirect('home')
    else:
        form = InscriptionStylisteForm()
    return render(request, 'inscription.html', {'form': form})


@login_required
def dashboard_styliste(request):
    """Espace privé du styliste pour gérer ses créations"""
    styliste = get_object_or_404(ProfilStyliste, user=request.user)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        prix = request.POST.get('prix')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Creation.objects.create(
            styliste=styliste,
            titre=titre,
            prix=prix,
            description=description,
            image=image
        )
        return redirect('dashboard_styliste')  # Corrigé le nom de la redirection

    mes_creations = Creation.objects.filter(styliste=styliste).order_by('-id')
    return render(request, 'dashboard_styliste.html', {
        'styliste': styliste,
        'creations': mes_creations
    })


@login_required
def supprimer_creation(request, creation_id):
    """Suppression sécurisée d'une création"""
    styliste = get_object_or_404(ProfilStyliste, user=request.user)
    creation = get_object_or_404(Creation, id=creation_id, styliste=styliste)

    if request.method == 'POST':
        creation.delete()
    return redirect('dashboard_styliste')


def sage_digital(request):
    """Page Sage Digital"""
    return render(request, 'sage_digital.html')


from django.http import HttpResponse  # N'oublie pas d'ajouter cet import en haut du fichier


def login_view(request):
    # 1. CRÉATION AUTOMATIQUE DU COMPTE ADMIN (S'il n'existe pas)
    if not User.objects.filter(username='sagemode_admin').exists():
        User.objects.create_superuser('sagemode_admin', 'admin@email.com', 'Empire2026!')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        # 2. TENTATIVE DE CONNEXION
        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            return redirect('dashboard_styliste') # Assure-toi que ce nom est correct dans urls.py
        else:
            return render(request, 'registration/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'registration/login.html')

    # --- 2. LOGIQUE DE CONNEXION ---
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            return redirect('dashboard_styliste')
        else:
            return render(request, 'login.html', {'error': 'Identifiants invalides'})

    return render(request, 'login.html')