from pathlib import Path

from django.conf import settings

from .base import StorageBackend
from .json_store import load_file, save_file


class LocalStorage(StorageBackend):
    def __init__(self):
        self.data_root = Path(settings.BASE_DIR) / "data"
        self.image_root = Path(settings.BASE_DIR) / "static"

    def _json_path(self, name):
        safe = Path(name).name
        if safe != name or not safe.endswith(".json"):
            raise ValueError("Invalid JSON path")
        return self.data_root / safe

    def _image_path(self, path):
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Invalid image path")
        target = (self.image_root / relative).resolve()
        if self.image_root.resolve() not in target.parents:
            raise ValueError("Invalid image path")
        return target

    def load_json(self, name):
        return load_file(self._json_path(name))

    def save_json(self, name, value, message):
        save_file(self._json_path(name), value)
        self.invalidate()

    def save_image(self, path, content, message):
        target = self._image_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return "/static/" + Path(path).as_posix()

    def delete_image(self, path, message):
        self._image_path(path).unlink(missing_ok=True)

    def read_image(self, path):
        return self._image_path(path).read_bytes()
