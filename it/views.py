from django.shortcuts import render, redirect, get_object_or_404
from .models import UsersIT
from .forms import UsersITForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import Group

@login_required(login_url="login")
def dashboard_it(request):
    # Check if the user is a member of the 'it_group'
    it_group = Group.objects.get(name='it_group')
    if request.user.groups.filter(name=it_group).exists():
        # If the user is in the 'it_group', render the dashboard-it.html template
        hardware = UsersIT.objects.all()
        return render(request, 'dashboard-it.html', {'hardware': hardware})
    else:
        # If the user is not in the 'it_group', redirect to a different page or display an error message
        return render(request, 'error-it.html', {'message': 'Access denied. You are not authorized to view this page.'})


def user_detail_it(request, user_id):
    user = get_object_or_404(UsersIT, pk=user_id)
    return render(request, 'detail-it.html', {'user': user})


@login_required(login_url="login")
def search_it(request):
    searched = request.POST.get("searched", "").lower()
    my_contracts = UsersIT.objects.filter(contractor__name__icontains=searched)
    if not my_contracts:
        message = f"<b> Nie znaleziono użytkownika '{searched}'.</b>"
    else:
        message = ""
    return render(request, "search-it.html", {"searched": searched, "my_contracts": my_contracts, "message": message})


@login_required(login_url="login")
def update_user_it(request, user_id):
    # Check if the user is a member of the 'it_group'
    it_group = Group.objects.get(name='it_group')
    if not request.user.groups.filter(name=it_group).exists():
        # If the user is not in the 'it_group', display an error message
        return render(request, 'error-it.html', {'message': 'Access denied. You are not authorized to perform this action.'})

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
