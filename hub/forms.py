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

    class Meta:
        model = ProfilStyliste
        fields = ['nom_marque', 'contact_whatsapp', 'photo_profil']