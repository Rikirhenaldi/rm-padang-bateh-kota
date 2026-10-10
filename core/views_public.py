from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render

from .services import get_storage
from .services.content import ContentService


def _context():
    service = ContentService()
    return {"service": service, "categories": service.categories(), "menus": service.menus(), "gallery_items": service.gallery()}


def home(request):
    context = _context()
    context["featured_menus"] = [item for item in context["menus"] if item.get("featured")]
    return render(request, "home.html", context)


def menu(request):
    context = _context()
    context["selected_category"] = request.GET.get("kategori", "")
    return render(request, "menu.html", context)


def gallery(request):
    return render(request, "gallery.html", _context())


def location(request):
    return render(request, "location.html", _context())


def contact(request):
    return render(request, "contact.html", _context())


def media(request, path):
    if ".." in path or path.startswith("/") or not path.startswith("images/"):
        raise Http404
    try:
        content = get_storage().read_image(path)
    except (FileNotFoundError, ValueError):
        raise Http404
    response = HttpResponse(content, content_type="image/octet-stream")
    response["Cache-Control"] = "public, max-age=86400"
    return response


def healthz(request):
    return HttpResponse("ok")
