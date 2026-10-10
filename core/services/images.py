import re
import secrets
from pathlib import PurePosixPath

from .base import StorageError

MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAGIC = {
    ".jpg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    ".webp": lambda data: data[:4] == b"RIFF" and data[8:12] == b"WEBP",
}


def safe_upload(upload):
    if not upload or upload.size > MAX_IMAGE_SIZE:
        raise StorageError("Image must be 5 MB or smaller")
    original = str(upload.name).replace("\\", "/")
    source = PurePosixPath(original)
    if source.is_absolute() or ".." in source.parts or "\x00" in original:
        raise StorageError("Invalid image filename")
    suffix = source.suffix.lower()
    if suffix not in MAGIC:
        raise StorageError("Only JPG, JPEG, PNG, and WEBP images are allowed")
    content = upload.read()
    if len(content) > MAX_IMAGE_SIZE or not MAGIC[suffix](content):
        raise StorageError("The uploaded file is not a valid supported image")
    stem = re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-")[:60] or "image"
    filename = f"{stem}-{secrets.token_hex(4)}{suffix}"
    return filename, content
