from django.conf import settings
from django.http import HttpResponsePermanentRedirect

CANONICAL_HOST = "www.sage-empire.com"
HEALTH_PATHS = ("/health", "/healthz")


class CanonicalHostMiddleware:
    """En production : sage-empire.onrender.com -> www.sage-empire.com (301, GET/HEAD
    uniquement, hors health checks). Le domaine nu sage-empire.com est déjà redirigé vers
    www par Cloudflare : ne JAMAIS rediriger www vers le domaine nu (boucle infinie).
    Les autres hôtes (localhost, testserver...) ne sont pas redirigés."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG:
            host = request.get_host().split(":")[0].lower()
            path = request.path
            is_health = path.rstrip("/") in HEALTH_PATHS
            redirect = False
            if host == "sage-empire.onrender.com":
                redirect = request.method in ("GET", "HEAD") and not is_health
            if redirect:
                return HttpResponsePermanentRedirect(
                    f"https://{CANONICAL_HOST}{request.get_full_path()}"
                )
        return self.get_response(request)
