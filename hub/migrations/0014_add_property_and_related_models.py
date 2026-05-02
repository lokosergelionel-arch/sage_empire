from django.db import models
import cloudinary.models
from django.utils.timezone import now


class Migration(models.Migration):
    dependencies = [
        ('hub', '0013_alter_profilstyliste_user_profilproprietaire_and_more'),
    ]

    operations = [
        models.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('type_bien', models.CharField(choices=[('appartement_meuble', 'Appartement Meublé'), ('villa_meublee', 'Villa Meublée')], max_length=30)),
                ('description', models.TextField(blank=True)),
                ('prix', models.DecimalField(decimal_places=0, max_digits=12)),
                ('quartier', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('draft', 'Brouillon'), ('pending', 'En attente de validation'), ('published', 'Publié'), ('rejected', 'Rejeté')], default='pending', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=models.CASCADE, related_name='properties', to='hub.profilproprietaire')),
            ],
            options={
                'verbose_name': 'Bien Immobilier',
                'verbose_name_plural': 'Biens Immobiliers',
                'ordering': ['-date_creation'],
            },
        ),
        models.CreateModel(
            name='PropertyMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('is_video', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('validated', models.BooleanField(default=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=models.CASCADE, related_name='medias', to='hub.property')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        models.CreateModel(
            name='PropertyAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=models.CASCADE, related_name='availabilities', to='hub.property')),
            ],
            options={
                'verbose_name': 'Disponibilité',
                'verbose_name_plural': 'Disponibilités',
                'ordering': ['start_date'],
            },
        ),
        models.CreateModel(
            name='VisitRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_name', models.CharField(max_length=100)),
                ('visitor_phone', models.CharField(max_length=20)),
                ('visitor_message', models.TextField(blank=True)),
                ('requested_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=0, default=5000, max_digits=10)),
                ('status', models.CharField(choices=[('new', 'Nouvelle'), ('contacted', 'Contacté'), ('done', 'Terminé')], default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=models.CASCADE, related_name='visit_requests', to='hub.property')),
            ],
        ),
        models.CreateModel(
            name='InvitationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('proprietaire', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='hub.profilproprietaire')),
            ],
        ),
    ]