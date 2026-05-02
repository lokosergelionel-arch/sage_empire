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

# ===================== FORMULAIRES STYLISTES =====================

class InscriptionStylisteForm(forms.ModelForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: empire_styliste'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@gmail.com'})
    )

    class Meta:
        model = ProfilStyliste
        fields = ['username', 'email', 'password', 'nom_marque', 'contact_whatsapp', 'photo_profil', 'biographie']

        widgets = {
            'nom_marque': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de votre Marque'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 22891645869'}),
            'biographie': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Parlez de vos inspirations...'}),
        }

        labels = {
            'nom_marque': 'Nom de la Marque / Maison',
            'contact_whatsapp': 'Numéro WhatsApp Pro',
            'biographie': 'Votre Univers / Biographie',
        }

class EditProfilForm(forms.ModelForm):
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@gmail.com'})
    )

    class Meta:
        model = ProfilStyliste
        fields = ['email', 'nom_marque', 'photo_profil', 'biographie', 'contact_whatsapp']

        widgets = {
            'nom_marque': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau nom de votre maison...'}),
            'biographie': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Parlez de vos inspirations...'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 22891645869'}),
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
        fields = ['titre', 'description', 'prix', 'disponible', 'image_url', 'image_dos_url']

        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Robe de soirée Empire'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez votre création...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_dos_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ===================== FORMULAIRES PROPRIETAIRE =====================

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['titre', 'type_bien', 'description', 'prix', 'quartier', 'status', 'is_active']

        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Villa Luxe à Cocody'}),
            'type_bien': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Décrivez le bien en détail...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix en FCFA'}),
            'quartier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cocody, Plateau, Riviera...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'titre': 'Titre du bien',
            'type_bien': 'Type de bien',
            'description': 'Description',
            'prix': 'Prix (FCFA)',
            'quartier': 'Quartier / Localisation',
            'status': 'Statut (pending, published, etc.)',
            'is_active': 'Bien actif',
        }

class PropertyAvailabilityForm(forms.ModelForm):
    class Meta:
        model = PropertyAvailability
        fields = ['start_date', 'end_date', 'is_available']

        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'is_available': 'Disponible',
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
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@gmail.com'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ProfilProprietaire
        fields = ['nom_complet', 'email', 'password', 'contact_whatsapp', 'photo_profil', 'biographie']

        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2250708091011'}),
            'biographie': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Présentez-vous brièvement...'}),
        }

        labels = {
            'nom_complet': 'Nom Complet',
            'contact_whatsapp': 'Numéro WhatsApp',
            'photo_profil': 'Photo de Profil',
            'biographie': 'Biographie / Présentation',
        }