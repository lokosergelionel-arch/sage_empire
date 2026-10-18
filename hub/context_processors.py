from django.conf import settings


def site_info(request):
    return {
        "SITE_URL": getattr(settings, "SITE_URL", "https://sage-empire.com"),
        "SITE_NAME": "SAGE EMPIRE",
    }
