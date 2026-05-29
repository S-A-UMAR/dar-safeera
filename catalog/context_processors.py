from django.conf import settings


def site_settings(request):
    """Injects brand settings into every template context."""
    return {
        'WHATSAPP_NUMBER': getattr(settings, 'WHATSAPP_NUMBER', '2347068886422'),
        'INSTAGRAM_HANDLE': getattr(settings, 'INSTAGRAM_HANDLE', 'safeeraabba'),
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', 'contact.safeeraabba@gmail.com'),
    }
