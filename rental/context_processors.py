def recaptcha(request):
    """context processor to add alerts to the site"""
    from django.conf import settings

    return {
        'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
