from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import render, redirect
from telefony.forms import AddRecordFormTelefony, \
    UpdateRecordFormTelefony, SmsRecordFormTelefony
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Task
from smsapi.client import SmsApiPlClient
from django.core.paginator import Paginator
from django.http import FileResponse
import io, os
from datetime import date, datetime
from django.db import connection
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage






@login_required(login_url="login")
def dashboard_todo(request):
    return render(request, 'dashboard-task.html')


@login_required(login_url="login")
def dashboard_todo_ce(request):
    tasks = Task.objects.all().filter(administracja__contains="CE") | Task.objects.all().filter(employee__username__contains="budziaka")
    return render(request, 'dashboard-todo-ce.html', {'tasks': tasks})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'list_task.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})