from django import forms
from django.contrib.auth.models import User
from .models import (
    ProfilStyliste,
    Creation,
    ProfilProprietaire,
    Property,
    PropertyAvailability,
    InvitationCode
)


# ===================== FORMULAIRES STYLISTES (EXISTANTS) =====================

class InscriptionStylisteForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'placeholder': 'exemple@gmail.com'}),
        required=True
    )

    nom_marque = forms.CharField(label="Nom de votre Marque")
    whatsapp = forms.CharField(label="Numéro WhatsApp")
    biographie = forms.CharField(
        label="Votre Biographie / Univers",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Parlez de vos inspirations...'}),
        required=False
    )

    class Meta:
        model = ProfilStyliste
        fields = ['nom_marque', 'contact_whatsapp', 'photo_profil', 'biographie']


class EditProfilForm(forms.ModelForm):
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'placeholder': 'exemple@gmail.com'}),
        required=True
    )

    class Meta:
        model = ProfilStyliste
        fields = ['nom_marque', 'photo_profil', 'biographie', 'contact_whatsapp']

        widgets = {
            'nom_marque': forms.TextInput(attrs={'placeholder': 'Nouveau nom de votre maison...'}),
            'biographie': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Parlez de vos inspirations...'}),
            'contact_whatsapp': forms.TextInput(attrs={'placeholder': 'Ex: 22891645869'}),
        }

        labels = {
            'nom_marque': 'Nom de la Marque / Maison',
            'photo_profil': 'Photo de Profil',
            'biographie': 'Votre Univers / Biographie',
            'contact_whatsapp': 'Numéro WhatsApp Pro',
        }


class CreationForm(forms.ModelForm):
    class Meta:
        model = Creation
        fields = ['titre', 'description', 'prix', 'disponible']

        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Robe de soirée Empire'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez votre création...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ===================== NOUVEAUX FORMULAIRES - PROPRIETAIRE =====================

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['titre', 'type_bien', 'description', 'prix', 'quartier']

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Villa Luxe à Cocody'
            }),
            'type_bien': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Décrivez le bien en détail...'
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prix en FCFA'
            }),
            'quartier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Cocody, Plateau, Riviera...'
            }),
        }

        labels = {
            'titre': 'Titre du bien',
            'type_bien': 'Type de bien',
            'description': 'Description',
            'prix': 'Prix (FCFA)',
            'quartier': 'Quartier / Localisation',
        }


class PropertyAvailabilityForm(forms.ModelForm):
    class Meta:
        model = PropertyAvailability
        fields = ['start_date', 'end_date', 'is_available']

        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_available': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'is_available': 'Statut de la période',
        }


class InvitationCodeForm(forms.Form):
    code = forms.CharField(
        label="Code d'invitation",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre code ici',
            'style': 'text-transform: uppercase;'
        }),
        max_length=20
    )


class CompleteProprietaireForm(forms.ModelForm):
    """Formulaire pour compléter l'inscription après validation du code"""

    class Meta:
        model = ProfilProprietaire
        fields = ['nom_complet', 'contact_whatsapp', 'photo_profil', 'biographie']

        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'contact_whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2250708091011'
            }),
            'biographie': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Présentez-vous brièvement...'
            }),
        }

        labels = {
            'nom_complet': 'Nom Complet',
            'contact_whatsapp': 'Numéro WhatsApp',
            'photo_profil': 'Photo de Profil',
            'biographie': 'Biographie / Présentation',
        }