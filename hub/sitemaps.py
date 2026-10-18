from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import ProfilProprietaire, ProfilStyliste, Property


class _CanonicalSite:
    domain = "sage-empire.com"
    name = "SAGE EMPIRE"


class CanonicalSitemap(Sitemap):
    """Force le domaine canonique (sans www) quel que soit l'hôte de la requête."""
    protocol = "https"

    def get_urls(self, page=1, site=None, protocol=None):
        return super().get_urls(page=page, site=_CanonicalSite(), protocol="https")


class StaticViewSitemap(CanonicalSitemap):
    changefreq = "monthly"
    protocol = "https"

    PRIORITIES = {
        "home": 1.0,
        "evenementiel": 0.9,
        "immobilier": 0.9,
        "sage_digital": 0.9,
        "galerie_mode": 0.9,
        "liste_stylistes": 0.8,
        "cgu": 0.3,
        "politique": 0.3,
    }

    def items(self):
        return list(self.PRIORITIES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES[item]


class StylisteSitemap(CanonicalSitemap):
    """Mêmes critères que l'annuaire public (liste_stylistes)."""
    changefreq = "weekly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return (
            ProfilStyliste.objects.filter(user__is_active=True, nom_marque__isnull=False)
            .exclude(nom_marque="")
            .exclude(user__username__in=["admin", "sagemode_admin"])
            .order_by("id")
        )

    def location(self, obj):
        return reverse("portfolio_styliste", args=[obj.id])


class ProprietaireSitemap(CanonicalSitemap):
    """Propriétaires vérifiés ayant au moins un bien publié et actif."""
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        ids = (
            Property.objects.filter(status="published", is_active=True)
            .values_list("owner_id", flat=True)
        )
        return ProfilProprietaire.objects.filter(est_verifie=True, id__in=ids).order_by("id")

    def location(self, obj):
        return reverse("portfolio_proprietaire", args=[obj.id])


sitemaps = {
    "static": StaticViewSitemap,
    "stylistes": StylisteSitemap,
    "proprietaires": ProprietaireSitemap,
}
