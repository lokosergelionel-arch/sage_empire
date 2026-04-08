from django import forms
from django.contrib.auth.models import User
from .models import ProfilStyliste


class InscriptionStylisteForm(forms.ModelForm):
    # Champs pour le compte (Logins)
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    # Champs pour le profil SAGE EMPIRE
    nom_marque = forms.CharField(label="Nom de votre Marque")
    whatsapp = forms.CharField(label="Numéro WhatsApp")

    # AJOUT : Champ Biographie pour qu'il apparaisse dans le formulaire
    biographie = forms.CharField(
        label="Votre Biographie / Univers",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Parlez de vos inspirations...'}),
        required=False
    )

    class Meta:
        model = ProfilStyliste
        # ON AJOUTE 'biographie' ICI POUR QU'IL SOIT ENREGISTRÉ
        fields = ['nom_marque', 'contact_whatsapp', 'photo_profil', 'biographie']