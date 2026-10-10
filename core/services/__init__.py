from django.conf import settings

from .github_storage import GitHubStorage
from .local_storage import LocalStorage

_storage = None


def get_storage():
    global _storage
    if _storage is None:
        _storage = GitHubStorage() if settings.STORAGE_BACKEND.lower() == "github" else LocalStorage()
    return _storage
