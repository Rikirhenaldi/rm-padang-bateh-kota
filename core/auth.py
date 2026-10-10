import hashlib
import hmac
import time

from django.conf import settings


def authenticate(username, password):
    return hmac.compare_digest(username or "", settings.ADMIN_USERNAME) and hmac.compare_digest(password or "", settings.ADMIN_PASSWORD)


def login(request, username):
    request.session.cycle_key()
    request.session["admin_auth"] = True
    request.session["admin_user"] = username
    request.session["auth_epoch"] = settings.AUTH_EPOCH
    request.session["issued_at"] = int(time.time())


def logout(request):
    request.session.flush()


def is_authenticated(request):
    return request.session.get("admin_auth") is True and hmac.compare_digest(request.session.get("auth_epoch", ""), settings.AUTH_EPOCH)
