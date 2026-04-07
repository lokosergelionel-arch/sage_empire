from django.db import models
from django.contrib.auth.models import User

# --- MODE ---
class ProfilStyliste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_marque = models.CharField(max_length=100)
    contact_whatsapp = models.CharField(max_length=20)
    photo_profil = models.ImageField(upload_to='profils/', null=True, blank=True)
    biographie = models.TextField(blank=True, help_text="Présentez votre parcours et votre style.")

    def __str__(self):
        return self.nom_marque

class Creation(models.Model):
    styliste = models.ForeignKey(ProfilStyliste, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='creations/')
    # AJOUT UNIQUEMENT ICI : L'image pour le dos (optionnelle pour ne pas bloquer tes anciens posts)
    image_dos = models.ImageField(upload_to='creations/', null=True, blank=True)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    disponible = models.BooleanField(default=True)
    date_post = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.prix} CFA"

# --- IMMOBILIER ---
class Immobilier(models.Model):
    CHOIX = [('terrain', 'Terrain'), ('apparte', 'Appartement')]
    type_bien = models.CharField(max_length=20, choices=CHOIX)
    titre = models.CharField(max_length=200)
    prix = models.CharField(max_length=100)
    image = models.ImageField(upload_to='immo/')

    def __str__(self):
        return self.titre

# --- ÉVÉNEMENTIEL ---
class Event(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.titre