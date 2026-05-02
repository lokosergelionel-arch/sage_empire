from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.timezone import now


# ===================== PROFILS =====================

class ProfilStyliste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_styliste')
    nom_marque = models.CharField(max_length=100)
    contact_whatsapp = models.CharField(max_length=20)
    photo_profil = CloudinaryField('image', null=True, blank=True)
    biographie = models.TextField(blank=True)
    email_verifie = models.BooleanField(default=False)
    date_inscription = models.DateTimeField(default=now)

    @property
    def get_photo_url(self):
        if self.photo_profil:
            try:
                return self.photo_profil.url
            except:
                return f"https://ui-avatars.com/api/?name={self.nom_marque}&background=f9f8f6&color=b5935e"
        return f"https://ui-avatars.com/api/?name={self.nom_marque}&background=f9f8f6&color=b5935e"

    def __str__(self):
        return self.nom_marque


class ProfilProprietaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_proprietaire')
    nom_complet = models.CharField(max_length=150)
    contact_whatsapp = models.CharField(max_length=20)
    photo_profil = CloudinaryField('image', null=True, blank=True)
    biographie = models.TextField(blank=True)
    date_inscription = models.DateTimeField(default=now)
    est_verifie = models.BooleanField(default=False)          # Validé par l'admin

    @property
    def get_photo_url(self):
        if self.photo_profil:
            try:
                return self.photo_profil.url
            except:
                return f"https://ui-avatars.com/api/?name={self.nom_complet}&background=1a1a1a&color=b8860b"
        return f"https://ui-avatars.com/api/?name={self.nom_complet}&background=1a1a1a&color=b8860b"

    def __str__(self):
        return self.nom_complet


# ===================== STYLISTES - CREATIONS =====================

class Creation(models.Model):
    styliste = models.ForeignKey(ProfilStyliste, on_delete=models.CASCADE, related_name='creations')
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='creations/', null=True, blank=True)
    image_dos = models.ImageField(upload_to='creations/', null=True, blank=True)
    public_id = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    image_dos_url = models.URLField(max_length=500, blank=True, null=True)
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
        return self.image_url or (self.image.url if self.image else None)

    @property
    def display_image_dos(self):
        return self.image_dos_url or (self.image_dos.url if self.image_dos else None)

    def __str__(self):
        return f"{self.titre} - {self.styliste.nom_marque}"

    def delete(self, *args, **kwargs):
        if self.public_id:
            try:
                import cloudinary.uploader
                cloudinary.uploader.destroy(self.public_id)
            except:
                pass
        super().delete(*args, **kwargs)


# ===================== IMMOBILIER (NOUVEAU SYSTÈME) =====================

class Property(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En attente de validation'),
        ('published', 'Publié'),
        ('rejected', 'Rejeté'),
    ]

    TYPE_CHOICES = [
        ('appartement_meuble', 'Appartement Meublé'),
        ('villa_meublee', 'Villa Meublée'),
    ]

    owner = models.ForeignKey(ProfilProprietaire, on_delete=models.CASCADE, related_name='properties')
    titre = models.CharField(max_length=200)
    type_bien = models.CharField(max_length=30, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=12, decimal_places=0)
    quartier = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bien Immobilier"
        verbose_name_plural = "Biens Immobiliers"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.owner.nom_complet}"


class PropertyMedia(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='medias')
    image = CloudinaryField('image')
    is_video = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    validated = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Media {self.id} - {self.property.titre}"


class PropertyAvailability(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"

    def __str__(self):
        return f"{self.property.titre} - {self.start_date} à {self.end_date}"


class VisitRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='visit_requests')
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=20)
    visitor_message = models.TextField(blank=True)
    requested_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=0, default=5000)
    status = models.CharField(max_length=20, default='new', choices=[
        ('new', 'Nouvelle'),
        ('contacted', 'Contacté'),
        ('done', 'Terminé')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande pour {self.property.titre} - {self.visitor_name}"


class InvitationCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    proprietaire = models.ForeignKey(ProfilProprietaire, on_delete=models.CASCADE, null=True, blank=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code


# ===================== ANCIEN MODÈLE (à migrer ou supprimer plus tard) =====================

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