from .services.content import ContentService


def site_context(request):
    service = ContentService()
    return {"restaurant": service.restaurant(), "site_settings": service.settings()}
