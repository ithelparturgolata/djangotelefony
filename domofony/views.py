from django.shortcuts import render, redirect
from .forms import TaskFormIntercom
from django.shortcuts import render
from .models import TaskIntercom


def add_task_intercom(request):
    if request.method == 'POST':
        form = TaskFormIntercom(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or do something else on successful form submission
    else:
        form = TaskFormIntercom()
    return render(request, 'add-intercom.html', {'form': form})
    # if request.method == 'POST':
    #     form = TaskFormIntercom(request.POST)
    #     if form.is_valid():
    #         task = form.save()
    #         # Code to send SMS to contractor using task.contractor.phone_number
    #         return redirect('task_added_successfully')  # Redirect to success page
    # else:
    #     form = TaskFormIntercom()
    # return render(request, 'add-intercom.html', {'form': form})



def dashboard_intercom(request):
    tasks = TaskIntercom.objects.all()
    return render(request, 'dashboard-intercom.html', {'tasks': tasks})