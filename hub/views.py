from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import ProfilStyliste, Creation, Immobilier, Event
from .forms import InscriptionStylisteForm, CreationForm


def home(request):
    creations = Creation.objects.all().order_by('-id')[:6]
    return render(request, 'index.html', {'creations': creations})


def page_immobilier(request):
    biens = Immobilier.objects.all()
    return render(request, 'immobilier.html', {'biens': biens})


def page_evenementiel(request):
    evenements = Event.objects.all().order_by('-date')
    return render(request, 'evenementiel.html', {'evenements': evenements})


def galerie_mode(request):
    creations = Creation.objects.all().order_by('-id')
    return render(request, 'galerie_mode.html', {'produits_sage': creations})


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
                if creation.public_id:
                    creation.public_id += f",{request.POST.get('public_id_dos')}"
                else:
                    creation.public_id = request.POST.get('public_id_dos')

            creation.save()
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


def login_view(request):
    if not User.objects.filter(username='sagemode_admin').exists():
        User.objects.create_superuser('sagemode_admin', 'admin@email.com', 'Empire2026!')

    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard_styliste')
        return render(request, 'registration/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'registration/login.html')


def sage_digital(request):
    return render(request, 'sage_digital.html')