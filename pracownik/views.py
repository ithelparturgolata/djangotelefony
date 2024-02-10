from .forms import ZadanieForm
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import Zadanie



@login_required(login_url="login")
def dashboard_todo(request):
    return render(request, 'dashboard-todo.html')


@login_required(login_url="login")
def dashboard_todo_ce(request):
    tasks = Zadanie.objects.all()
    return render(request, 'dashboard-todo-ce.html', {'tasks': tasks})


def task_list(request):
    tasks = Zadanie.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = ZadanieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = ZadanieForm()
    return render(request, 'add_task.html', {'form': form})

def edit_task(request, task_id):
    task = Zadanie.objects.get(id=task_id)
    if request.method == 'POST':
        form = ZadanieForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = ZadanieForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})