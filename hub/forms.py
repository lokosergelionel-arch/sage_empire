from django import forms
from django.contrib.auth.models import User
from .models import ProfilStyliste, Creation


class InscriptionStylisteForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    # === Email ajouté et obligatoire à l'inscription ===
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
    # === Email ajouté pour pouvoir le modifier ===
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