import json
import os
import tempfile
from pathlib import Path

from .base import StorageError


def load_file(path):
    try:
        with Path(path).open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError(f"Unable to load {path}: {exc}") from exc


def save_file(path, value):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            temporary = handle.name
        os.replace(temporary, destination)
    except OSError as exc:
        if "temporary" in locals():
            Path(temporary).unlink(missing_ok=True)
        raise StorageError(f"Unable to save {path}: {exc}") from exc
