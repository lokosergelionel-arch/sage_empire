from django import forms
from django.contrib.auth.models import User
from .models import ProfilStyliste, Creation  # <-- MODIFIÉ : On importe aussi Creation ici

class InscriptionStylisteForm(forms.ModelForm):
    # Champs pour le compte (Logins)
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    # Champs pour le profil SAGE EMPIRE
    nom_marque = forms.CharField(label="Nom de votre Marque")
    whatsapp = forms.CharField(label="Numéro WhatsApp")

    # AJOUT : Champ Biographie
    biographie = forms.CharField(
        label="Votre Biographie / Univers",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Parlez de vos inspirations...'}),
        required=False
    )

    class Meta:
        model = ProfilStyliste
        # On utilise les noms exacts de ton models.py
        fields = ['nom_marque', 'contact_whatsapp', 'photo_profil', 'biographie']


class CreationForm(forms.ModelForm):
    class Meta:
        model = Creation
        # Les champs correspondent à ton models.py
        fields = ['titre', 'image', 'image_dos', 'description', 'prix', 'disponible']

        # Widgets pour le style Bootstrap (propre et net)
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Robe de soirée Empire'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Décrivez votre création...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_dos': forms.FileInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }