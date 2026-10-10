from django.contrib import messages
from django.shortcuts import redirect, render

from .auth import authenticate, is_authenticated, login, logout


def login_view(request):
    if is_authenticated(request):
        return redirect("dashboard")
    if request.method == "POST":
        if authenticate(request.POST.get("username"), request.POST.get("password")):
            login(request, request.POST.get("username"))
            destination = request.GET.get("next", "/dashboard/")
            if not destination.startswith("/") or destination.startswith("//"):
                destination = "/dashboard/"
            return redirect(destination)
        messages.error(request, "Username atau password salah.")
    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return redirect("dashboard-login")
