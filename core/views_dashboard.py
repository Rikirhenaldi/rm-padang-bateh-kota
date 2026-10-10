from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import admin_required
from .services.content import ContentService
from .services.images import safe_upload


def service():
    return ContentService()


@admin_required
def index(request):
    content = service()
    return render(request, "dashboard/index.html", {"menus": content.menus(include_unavailable=True), "categories": content.all_categories(), "gallery_items": content.gallery()})


@admin_required
def restaurant(request):
    content = service()
    if request.method == "POST":
        data = {key: request.POST.get(key, "") for key in ["name", "tagline", "description", "logo", "address", "phone", "whatsapp", "shopee_url", "google_maps_url", "instagram", "facebook", "tiktok"]}
        data["opening_hours"] = [{"days": request.POST.get("opening_days", "Setiap hari"), "hours": request.POST.get("opening_hours", "")}]
        content.save_restaurant(data)
        messages.success(request, "Profil restoran disimpan.")
        return redirect("dashboard-restaurant")
    return render(request, "dashboard/restaurant.html", {"item": content.restaurant()})


@admin_required
def settings_view(request):
    content = service()
    if request.method == "POST":
        content.save_settings({"price_note": request.POST.get("price_note", ""), "show_price_note": "show_price_note" in request.POST, "home_menu_limit": int(request.POST.get("home_menu_limit", 11) or 11), "order_methods": [x.strip() for x in request.POST.get("order_methods", "").split(",") if x.strip()], "show_gallery": "show_gallery" in request.POST})
        messages.success(request, "Pengaturan disimpan.")
        return redirect("dashboard-settings")
    return render(request, "dashboard/settings.html", {"item": content.settings()})


@admin_required
def menu_list(request):
    content = service()
    return render(request, "dashboard/menu_list.html", {"items": content.menus(include_unavailable=True), "categories": content.all_categories()})


@admin_required
def menu_form(request, item_id=None):
    content = service()
    item = next((x for x in content.menus(include_unavailable=True) if x.get("id") == item_id), {})
    if request.method == "POST":
        data = {key: request.POST.get(key, "") for key in ["category_id", "name", "description", "price", "image", "plate_color", "plate_bg", "badge", "sort_order"]}
        data.update({"available": "available" in request.POST, "featured": "featured" in request.POST, "price_verified": "price_verified" in request.POST})
        try:
            content.save_menu(data, item_id)
            messages.success(request, "Menu disimpan.")
            return redirect("dashboard-menu")
        except (ValueError, TypeError) as exc:
            messages.error(request, str(exc))
            item = {**item, **data}
    return render(request, "dashboard/menu_form.html", {"item": item, "categories": content.all_categories()})


@admin_required
@require_POST
def menu_delete(request, item_id):
    service().delete_menu(item_id)
    messages.success(request, "Menu dihapus.")
    return redirect("dashboard-menu")


@admin_required
def category_list(request):
    return render(request, "dashboard/category_list.html", {"items": service().all_categories()})


@admin_required
def category_form(request, item_id=None):
    content = service()
    item = next((x for x in content.all_categories() if x.get("id") == item_id), {})
    if request.method == "POST":
        data = {key: request.POST.get(key, "") for key in ["name", "description", "sort_order"]}
        data["active"] = "active" in request.POST
        try:
            content.save_category(data, item_id)
            messages.success(request, "Kategori disimpan.")
            return redirect("dashboard-categories")
        except (ValueError, TypeError) as exc:
            messages.error(request, str(exc))
            item = {**item, **data}
    return render(request, "dashboard/category_form.html", {"item": item})


@admin_required
@require_POST
def category_delete(request, item_id):
    try:
        service().delete_category(item_id)
        messages.success(request, "Kategori dihapus.")
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect("dashboard-categories")


@admin_required
def gallery_list(request):
    return render(request, "dashboard/gallery.html", {"items": service().gallery()})


@admin_required
@require_POST
def gallery_upload(request):
    upload = request.FILES.get("image")
    try:
        filename, content = safe_upload(upload)
        path = f"images/gallery/{filename}"
        url = service().storage.save_image(path, content, "content: upload gallery image")
        document = service().read("gallery.json", {"images": []})
        document["images"].append({"id": filename.rsplit(".", 1)[0], "filename": filename, "url": url, "caption": request.POST.get("caption", "").strip(), "sort_order": len(document["images"]) + 1})
        service().save_document("gallery.json", document)
        messages.success(request, "Gambar diunggah.")
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect("dashboard-gallery")


@admin_required
@require_POST
def gallery_delete(request, item_id):
    content = service()
    document = content.read("gallery.json", {"images": []})
    target = next((x for x in document["images"] if x.get("id") == item_id), None)
    if target:
        if target.get("filename"):
            content.storage.delete_image(f"images/gallery/{target['filename']}", "content: delete gallery image")
        document["images"] = [x for x in document["images"] if x.get("id") != item_id]
        content.save_document("gallery.json", document)
    return redirect("dashboard-gallery")
