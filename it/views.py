from django.shortcuts import render, redirect, get_object_or_404
from .models import UsersIT
from .forms import UsersITForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group


@login_required(login_url="login")
def dashboard_it(request):
    """
    Display IT dashboard.

    This view displays the IT dashboard page, showing information about hardware for IT users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered dashboard-it.html template with hardware information or error-it.html
        if the user is not authorized to view the page.

    """
    it_group = Group.objects.get(name='it_group')
    if request.user.groups.filter(name=it_group).exists():
        hardware = UsersIT.objects.all()
        return render(request, 'dashboard-it.html', {'hardware': hardware})
    else:
        return render(request, 'error-it.html', {'message': 'Access denied. You are not authorized to view this page.'})


def user_detail_it(request, user_id):
    """
    Display details of a specific IT user.

    This view displays detailed information about a specific IT user.

    Args:
        request (HttpRequest): The request object.
        user_id (int): The ID of the user to display details for.

    Returns:
        HttpResponse: The rendered detail-it.html template with user details.

    Raises:
        Http404: If the specified user does not exist.

    """
    user = get_object_or_404(UsersIT, pk=user_id)
    return render(request, 'detail-it.html', {'user': user})


@login_required(login_url="login")
def search_it(request):
    """
    Search for IT users.

    This view allows searching for IT users based on contractor name.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered search-it.html template with search results.

    """
    searched = request.POST.get("searched", "").lower()
    my_contracts = UsersIT.objects.filter(contractor__name__icontains=searched)
    if not my_contracts:
        message = f"<b> Nie znaleziono użytkownika '{searched}'.</b>"
    else:
        message = ""
    return render(request, "search-it.html", {"searched": searched, "my_contracts": my_contracts, "message": message})


@login_required(login_url="login")
def update_user_it(request, user_id):
    """
    Update information of a specific IT user.

    This view allows updating information of a specific IT user.

    Args:
        request (HttpRequest): The request object.
        user_id (int): The ID of the user to update.

    Returns:
        HttpResponse: The rendered update-user-it.html template with the update form and user information.

    Raises:
        Http404: If the specified user does not exist.
        PermissionDenied: If the user does not have permission to update user information.

    """
    it_group = Group.objects.get(name='it_group')
    if not request.user.groups.filter(name=it_group).exists():
        return render(request, 'error-it.html',
                      {'message': 'Odmowa dostępu.'})

    user = get_object_or_404(UsersIT, pk=user_id)
    if request.method == 'POST':
        form = UsersITForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information updated successfully.')
            return redirect('user_detail_it', user_id=user_id)
    else:
        form = UsersITForm(instance=user)
    return render(request, 'update-user-it.html', {'form': form, 'user': user})
