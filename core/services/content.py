import re
from copy import deepcopy

from . import get_storage
from .base import StorageError


class ContentService:
    def __init__(self, storage=None):
        self.storage = storage or get_storage()

    def read(self, name, default):
        return self.storage.load_json(name) or deepcopy(default)

    def restaurant(self):
        return self.read("restaurant.json", {})

    def categories(self):
        items = self.read("categories.json", {"categories": []}).get("categories", [])
        return sorted((x for x in items if x.get("active", True)), key=lambda x: (x.get("sort_order", 9999), x.get("name", "")))

    def all_categories(self):
        items = self.read("categories.json", {"categories": []}).get("categories", [])
        return sorted(items, key=lambda x: (x.get("sort_order", 9999), x.get("name", "")))

    def menus(self, include_unavailable=False):
        items = self.read("menu.json", {"menus": []}).get("menus", [])
        if not include_unavailable:
            items = [x for x in items if x.get("available", True)]
        return sorted(items, key=lambda x: (x.get("sort_order", 9999), x.get("name", "")))

    def gallery(self):
        return sorted(self.read("gallery.json", {"images": []}).get("images", []), key=lambda x: x.get("sort_order", 9999))

    def settings(self):
        return self.read("settings.json", {"site": {}}).get("site", {})

    def save_document(self, name, value):
        self.storage.save_json(name, value, f"content: update {name}")

    def save_restaurant(self, data):
        current = self.restaurant()
        fields = ["name", "tagline", "description", "logo", "address", "phone", "whatsapp", "shopee_url", "google_maps_url", "latitude", "longitude", "opening_hours", "instagram", "facebook", "tiktok"]
        current.update({field: data.get(field, current.get(field, "")) for field in fields})
        self.save_document("restaurant.json", current)

    def save_settings(self, data):
        current = self.settings()
        current.update(data)
        self.save_document("settings.json", {"site": current})

    @staticmethod
    def slug(value):
        return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

    def save_menu(self, data, menu_id=None):
        document = self.read("menu.json", {"menus": []})
        items = document["menus"]
        item = {"id": menu_id or self.slug(data.get("name", "item")), "category_id": data.get("category_id", ""), "name": data.get("name", "").strip(), "description": data.get("description", "").strip(), "price": int(data.get("price", 0) or 0), "image": data.get("image") or None, "plate_color": data.get("plate_color", "#EE8A3A"), "plate_bg": data.get("plate_bg", "#F8D340"), "badge": data.get("badge", "").strip(), "available": bool(data.get("available", True)), "featured": bool(data.get("featured", False)), "price_verified": bool(data.get("price_verified", False)), "sort_order": int(data.get("sort_order", len(items) + 1) or len(items) + 1)}
        if not item["name"] or not item["category_id"]:
            raise ValueError("Menu name and category are required")
        if menu_id:
            for index, existing in enumerate(items):
                if existing.get("id") == menu_id:
                    items[index] = item
                    break
            else:
                raise ValueError("Menu not found")
        else:
            if any(existing.get("id") == item["id"] for existing in items):
                item["id"] += "-" + self.slug(item["name"])[-6:]
            items.append(item)
        self.save_document("menu.json", document)
        return item

    def delete_menu(self, menu_id):
        document = self.read("menu.json", {"menus": []})
        document["menus"] = [item for item in document["menus"] if item.get("id") != menu_id]
        self.save_document("menu.json", document)

    def save_category(self, data, category_id=None):
        document = self.read("categories.json", {"categories": []})
        items = document["categories"]
        item = {"id": category_id or self.slug(data.get("name", "category")), "name": data.get("name", "").strip(), "description": data.get("description", "").strip(), "active": bool(data.get("active", True)), "sort_order": int(data.get("sort_order", len(items) + 1) or len(items) + 1)}
        if not item["name"]:
            raise ValueError("Category name is required")
        if category_id:
            for index, existing in enumerate(items):
                if existing.get("id") == category_id:
                    items[index] = item
                    break
            else:
                raise ValueError("Category not found")
        else:
            if any(existing.get("id") == item["id"] for existing in items):
                raise ValueError("Category already exists")
            items.append(item)
        self.save_document("categories.json", document)
        return item

    def delete_category(self, category_id):
        menus = self.menus(include_unavailable=True)
        if any(item.get("category_id") == category_id for item in menus):
            raise ValueError("Category still has menu items")
        document = self.read("categories.json", {"categories": []})
        document["categories"] = [item for item in document["categories"] if item.get("id") != category_id]
        self.save_document("categories.json", document)
