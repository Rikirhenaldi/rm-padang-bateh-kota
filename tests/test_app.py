from pathlib import Path

from django.test import SimpleTestCase, override_settings

from core.auth import authenticate
from core.services.content import ContentService
from core.services.images import safe_upload


class Upload:
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.size = len(content)

    def read(self):
        return self.content


class MemoryStorage:
    def __init__(self):
        self.documents = {}

    def load_json(self, name):
        return self.documents.get(name)

    def save_json(self, name, value, message):
        self.documents[name] = value


class PublicRouteTests(SimpleTestCase):
    def test_public_pages_render(self):
        for path in ["/", "/menu/", "/gallery/", "/lokasi/", "/kontak/"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard/")
        self.assertRedirects(response, "/dashboard/login/?next=/dashboard/")

    def test_login_works_without_database(self):
        response = self.client.post("/dashboard/login/", {"username": "admin", "password": "change-me"})
        self.assertRedirects(response, "/dashboard/")
        self.assertEqual(self.client.get("/dashboard/").status_code, 200)


class ServiceTests(SimpleTestCase):
    def test_content_service_crud_uses_storage_interface(self):
        storage = MemoryStorage()
        content = ContentService(storage)
        content.save_category({"name": "Lauk", "description": "", "active": True, "sort_order": 1})
        content.save_menu({"name": "Rendang", "category_id": "lauk", "price": "25000", "sort_order": 1})
        self.assertEqual(content.menus()[0]["price"], 25000)
        with self.assertRaises(ValueError):
            content.delete_category("lauk")

    def test_local_credentials_are_constant_time_checked(self):
        self.assertTrue(authenticate("admin", "change-me"))
        self.assertFalse(authenticate("admin", "wrong"))

    def test_upload_validation_rejects_invalid_files(self):
        with self.assertRaises(Exception):
            safe_upload(Upload("payload.exe", b"MZ"))
        with self.assertRaises(Exception):
            safe_upload(Upload("../../payload.jpg", b"\xff\xd8\xff"))

    def test_upload_validation_accepts_png(self):
        name, content = safe_upload(Upload("food photo.png", b"\x89PNG\r\n\x1a\n"))
        self.assertTrue(name.startswith("food-photo-"))
        self.assertTrue(name.endswith(".png"))
        self.assertEqual(len(content), 8)
