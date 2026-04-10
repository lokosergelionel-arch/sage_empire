from django.db import models
from django.contrib.auth.models import User
import cloudinary.uploader


class ProfilStyliste(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil'
    )
    nom_marque = models.CharField(max_length=100)
    contact_whatsapp = models.CharField(max_length=20)
    photo_profil = models.ImageField(upload_to='profils/', null=True, blank=True)
    biographie = models.TextField(blank=True)

    def __str__(self):
        return self.nom_marque


class Creation(models.Model):
    styliste = models.ForeignKey(ProfilStyliste, on_delete=models.CASCADE, related_name='creations')
    titre = models.CharField(max_length=200)

    # Champs Cloudinary
    image = models.ImageField(upload_to='creations/', null=True, blank=True)
    image_dos = models.ImageField(upload_to='creations/', null=True, blank=True)
    public_id = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    image_dos_url = models.URLField(max_length=500, blank=True)  # ← NOUVEAU

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
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return None

    @property
    def display_image_dos(self):
        if self.image_dos_url:
            return self.image_dos_url
        if self.image_dos and self.image_dos.url:
            return self.image_dos.url
        return None

    def __str__(self):
        return f"{self.titre} - {self.styliste.nom_marque}"

    def delete(self, *args, **kwargs):
        if self.public_id:
            try:
                cloudinary.uploader.destroy(self.public_id)
            except:
                pass
        super().delete(*args, **kwargs)


# Anciens modèles conservés
class Immobilier(models.Model):
    CHOIX = [('terrain', 'Terrain'), ('appartement', 'Appartement')]
    type_bien = models.CharField(max_length=20, choices=CHOIX)
    titre = models.CharField(max_length=200)
    prix = models.CharField(max_length=100)
    image = models.ImageField(upload_to='immo/')
    public_id = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.titre


class Event(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    public_id = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.titre