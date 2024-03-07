from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import TaskForm
from .models import Task, TaskPhoto
from django.shortcuts import render, redirect


def dashboard_task(request):
    tasks = Task.objects.all()
    return render(request, 'dashboard-task.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


def task_detail(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        if 'additional_photo' in request.FILES:
            photo = TaskPhoto(image=request.FILES['additional_photo'], task=task)
            photo.save()
            return redirect('task_detail', task_id=task_id)
    return render(request, 'detail_task.html', {'task': task})