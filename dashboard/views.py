from django.shortcuts import render, redirect
from telefony.forms import CreateUserForm, LoginForm, \
    AddRecordFormTelefony, UpdateRecordFormTelefony, SmsRecordFormTelefony
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import pycodestyle
from telefony.models import Mieszkaniec
from smsapi.client import SmsApiPlClient
from django.core.paginator import Paginator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# homepage view
def home(request):
    return render(request, ("index.html"))


# register view
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}
    
    return render(request, "register.html", context=context)


# login view
def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Zalogowano")

                return redirect("dashboard")

    context = {"form": form}
    return render(request, "login.html", context=context)


# logout view
def logout_view(request):
    auth.logout(request)
    messages.success(request, "Wylogowano")
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):

    return render(request, "dashboard.html")


def dashboard_main(request):

    return render(request, "rss/../rss/templates/dashboard-main.html")
