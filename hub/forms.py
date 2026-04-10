from django import forms
from .models import ProfilStyliste, Creation


class InscriptionStylisteForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

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


class CreationForm(forms.ModelForm):
    class Meta:
        model = Creation
        fields = ['titre', 'description', 'prix', 'disponible']

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Robe de soirée Empire'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez votre création...'
            }),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }