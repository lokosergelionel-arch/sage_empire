from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField # Import officiel
import cloudinary.uploader


class ProfilStyliste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nom_marque = models.CharField(max_length=100)
    contact_whatsapp = models.CharField(max_length=20)
    # Utilisation de CloudinaryField pour la photo de profil
    photo_profil = CloudinaryField('profils', null=True, blank=True)
    biographie = models.TextField(blank=True)

    def __str__(self):
        return self.nom_marque


class Creation(models.Model):
    styliste = models.ForeignKey(ProfilStyliste, on_delete=models.CASCADE, related_name='creations')
    titre = models.CharField(max_length=200)

    # Utilisation correcte du champ Cloudinary
    image = CloudinaryField('creations', null=True, blank=True)
    image_dos = CloudinaryField('creations_dos', null=True, blank=True)

    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    disponible = models.BooleanField(default=True)
    date_post = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Création"
        verbose_name_plural = "Créations"
        ordering = ['-date_post']

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return ""

    @property
    def display_image_dos(self):
        if self.image_dos:
            return self.image_dos.url
        return ""

    def __str__(self):
        return f"{self.titre} - {self.styliste.nom_marque}"

    # CORRECTION DE LA SUPPRESSION
    def delete(self, *args, **kwargs):
        # Avec CloudinaryField, l'ID public est stocké directement dans le champ image
        if self.image:
            try:
                cloudinary.uploader.destroy(self.image.public_id)
            except:
                pass
        if self.image_dos:
            try:
                cloudinary.uploader.destroy(self.image_dos.public_id)
            except:
                pass
        super().delete(*args, **kwargs)


class Immobilier(models.Model):
    CHOIX = [('terrain', 'Terrain'), ('appartement', 'Appartement')]
    type_bien = models.CharField(max_length=20, choices=CHOIX)
    titre = models.CharField(max_length=200)
    prix = models.CharField(max_length=100)
    image = CloudinaryField('immo')

    def __str__(self):
        return self.titre


class Event(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    image = CloudinaryField('events', null=True, blank=True)

    def __str__(self):
        return self.titre