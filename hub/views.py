from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Import de tous tes modèles
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
    # On cherche le profil de votre propre marque
    # Assure-toi de créer un profil styliste avec exactement ce nom : "SAGE MODE"
    try:
        profil_sage = ProfilStyliste.objects.get(nom_marque="SAGE MODE")
        produits = Creation.objects.filter(styliste=profil_sage).order_by('-id')
    except ProfilStyliste.DoesNotExist:
        produits = [] # Si le profil n'existe pas encore, on n'affiche rien

    return render(request, 'galerie_mode.html', {'produits_sage': produits})


def liste_stylistes(request):
    # On récupère tous les stylistes SAUF "SAGE MODE"
    stylistes = ProfilStyliste.objects.exclude(nom_marque="SAGE MODE")
    return render(request, 'annuaire_stylistes.html', {'stylistes': stylistes})


def portfolio_styliste(request, styliste_id):
    styliste = get_object_or_404(ProfilStyliste, id=styliste_id)
    # Utilise 'Creation' ici aussi
    oeuvres = Creation.objects.filter(styliste=styliste).order_by('-id')

    return render(request, 'portfolio_styliste.html', {
        'styliste': styliste,
        'oeuvres': oeuvres  # On envoie la variable 'oeuvres' au HTML
    })


# --- 3. GESTION DES CRÉATEURS (INSCRIPTION & DASHBOARD) ---

def inscription_styliste(request):
    """Formulaire d'inscription pour les nouveaux partenaires"""
    if request.method == 'POST':
        form = InscriptionStylisteForm(request.POST, request.FILES)
        if form.is_valid():
            # Création de l'utilisateur Django
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # Création du profil lié
            profil = form.save(commit=False)
            profil.user = user
            profil.save()
            return redirect('home')
    else:
        form = InscriptionStylisteForm()
    return render(request, 'inscription.html', {'form': form})


@login_required
def dashboard_styliste(request):
    styliste = get_object_or_404(ProfilStyliste, user=request.user)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        prix = request.POST.get('prix')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # CORRECTION ICI AUSSI : On utilise Creation.objects.create
        Creation.objects.create(
            styliste=styliste,
            titre=titre,
            prix=prix,
            description=description,
            image=image
        )
        return redirect('dashboard')

    # ET ICI : filter(styliste=styliste)
    mes_creations = Creation.objects.filter(styliste=styliste).order_by('-id')

    return render(request, 'dashboard_styliste.html', {
        'styliste': styliste,
        'creations': mes_creations
    })


login_required


def supprimer_creation(request, creation_id):
    # 1. On vérifie qui est le styliste connecté
    styliste = get_object_or_404(ProfilStyliste, user=request.user)

    # 2. On cherche la création ET on vérifie qu'elle appartient bien à CE styliste
    creation = get_object_or_404(Creation, id=creation_id, styliste=styliste)

    if request.method == 'POST':
        creation.delete()  # On supprime

    return redirect('dashboard')  # On recharge le dashboard

def sage_digital(request):
    return render(request, 'sage_digital.html')