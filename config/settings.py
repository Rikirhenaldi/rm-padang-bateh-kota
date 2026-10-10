import hashlib
import importlib.util
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_SETTINGS = BASE_DIR / "local_settings.py"

if LOCAL_SETTINGS.exists():
    spec = importlib.util.spec_from_file_location("local_settings", LOCAL_SETTINGS)
    local = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(local)
    for key in dir(local):
        if key.isupper():
            globals()[key] = getattr(local, key)

SECRET_KEY = globals().get("SECRET_KEY", os.environ.get("SECRET_KEY", "dev-only-change-me"))
DEBUG = globals().get("DEBUG", os.environ.get("DEBUG", "True").lower() == "true")
ALLOWED_HOSTS = globals().get("ALLOWED_HOSTS", [x for x in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost,192.168.100.8").split(",") if x])
ADMIN_USERNAME = globals().get("ADMIN_USERNAME", os.environ.get("ADMIN_USERNAME", "admin"))
ADMIN_PASSWORD = globals().get("ADMIN_PASSWORD", os.environ.get("ADMIN_PASSWORD", "change-me"))
STORAGE_BACKEND = globals().get("STORAGE_BACKEND", os.environ.get("STORAGE_BACKEND", "local"))
GITHUB_TOKEN = globals().get("GITHUB_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
GITHUB_OWNER = globals().get("GITHUB_OWNER", os.environ.get("GITHUB_OWNER", ""))
GITHUB_REPOSITORY = globals().get("GITHUB_REPOSITORY", os.environ.get("GITHUB_REPOSITORY", ""))
GITHUB_BRANCH = globals().get("GITHUB_BRANCH", os.environ.get("GITHUB_BRANCH", "main"))

INSTALLED_APPS = ["django.contrib.messages", "django.contrib.staticfiles", "core"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.messages.context_processors.messages",
        "core.context_processors.site_context",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {}
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_AGE = 28800
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = not DEBUG
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}}
WHITENOISE_MANIFEST_STRICT = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "rm-padang"}}
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = globals().get("CSRF_TRUSTED_ORIGINS", [x for x in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if x])
AUTH_EPOCH = hashlib.sha256(f"{SECRET_KEY}|{ADMIN_USERNAME}|{ADMIN_PASSWORD}".encode()).hexdigest()[:32]
