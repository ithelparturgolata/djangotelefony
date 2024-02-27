from django.shortcuts import render, redirect
from telefony.forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    """
    Render the homepage view.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for the homepage.
    """
    return render(request, "index.html")


def register(request):
    """
    Render the registration form and handle user registration.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for the registration page.
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {"form": form}
    
    return render(request, "register.html", context=context)


def login_view(request):
    """
    Render the login form and authenticate user login.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for the login page.
    """
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        try:
            if form.is_valid():
                username = request.POST.get("username")
                password = request.POST.get("password")
                
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, "Zalogowano")
                    return redirect("dashboard")
                else:
                    raise ValueError("Invalid login or password")  # Raise ValueError for invalid login or password
        except ValueError as e:
            messages.error(request, str(e))  # Display error message
            return render(request, "login.html", {"form": form})  # Render login page with error message
    
    context = {"form": form}
    return render(request, "login.html", context=context)


def logout_view(request):
    """
    Log out the user and redirect to the login page.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponseRedirect: Redirect to the login page after logout.
    """
    auth.logout(request)
    messages.success(request, "Wylogowano")
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    """
    Render the dashboard view.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for the dashboard.
    """
    return render(request, "dashboard.html")


def dashboard_main(request):
    """
    Render the main dashboard view.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for the main dashboard.
    """
    return render(request, "dashboard-main.html")

# from django.shortcuts import render, redirect
# from telefony.forms import CreateUserForm, LoginForm
# from django.contrib.auth.models import auth
# from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
#
#
# def home(request):
#     """
#     Render the homepage view.
#
#     Parameters:
#     - request (HttpRequest): The HTTP request object.
#
#     Returns:
#     - HttpResponse: Rendered template for the homepage.
#     """
#     return render(request, "index.html")
#
#
# def register(request):
#     """
#     Render the registration form and handle user registration.
#
#     Parameters:
#     - request (HttpRequest): The HTTP request object.
#
#     Returns:
#     - HttpResponse: Rendered template for the registration page.
#     """
#     form = CreateUserForm()
#     if request.method == "POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#     context = {"form": form}
#
#     return render(request, "register.html", context=context)
#
#
# def login_view(request):
#     """
#     Render the login form and authenticate user login.
#
#     Parameters:
#     - request (HttpRequest): The HTTP request object.
#
#     Returns:
#     - HttpResponse: Rendered template for the login page.
#     """
#     form = LoginForm()
#
#     if request.method == "POST":
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = request.POST.get("username")
#             password = request.POST.get("password")
#
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 messages.success(request, "Zalogowano")
#                 return redirect("dashboard")
#             else:
#                 messages.error(request, "Nieprawidłowy login lub hasło")  # Display error message
#                 return render(request, "login.html", {"form": form})  # Render login page with error message
#
#     context = {"form": form}
#     return render(request, "login.html", context=context)
#
#
# def logout_view(request):
#     """
#     Log out the user and redirect to the login page.
#
#     Parameters:
#     - request (HttpRequest): The HTTP request object.
#
#     Returns:
#     - HttpResponseRedirect: Redirect to the login page after logout.
#     """
#     auth.logout(request)
#     messages.success(request, "Wylogowano")
#     return redirect("login")
#
#
# @login_required(login_url="login")
# def dashboard(request):
#     """
#     Render the dashboard view.
#
#     Parameters:
#     - request (HttpRequest): The HTTP request object.
#
#     Returns:
#     - HttpResponse: Rendered template for the dashboard.
#     """
#     return render(request, "dashboard.html")
#
#
# def dashboard_main(request):
#     """
#     Render the main dashboard view.
#
#     Parameters:
#     - request (HttpRequest): The HTTP request object.
#
#     Returns:
#     - HttpResponse: Rendered template for the main dashboard.
#     """
#     return render(request, "dashboard-main.html")
