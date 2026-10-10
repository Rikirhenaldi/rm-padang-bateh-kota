from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .auth import is_authenticated


def admin_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not is_authenticated(request):
            messages.info(request, "Silakan masuk untuk mengakses dashboard.")
            return redirect(f"/dashboard/login/?next={request.path}")
        return view(request, *args, **kwargs)

    return wrapped
