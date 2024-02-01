from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.template.loader import get_template
# from xhtml2pdf import pisa
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
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_summary')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required(login_url="login")
def dashboard_todo(request):
    return render(request, 'dashboard-todo.html')


@login_required(login_url="login")
def dashboard_todo_ce(request):
    tasks = Task.objects.all().filter(administracja__contains="CE")
    return render(request, 'dashboard-todo-ce.html', {'tasks': tasks})


@login_required(login_url="login")
def view_record(request, pk):
    all_records_todo = Task.objects.get(id=pk)
    context = {"records_todo": all_records_todo}

    return render(request, "task-view.html", context=context)


# def generate_pdf(request):
#     tasks = Task.objects.all()
#     template_path = 'task_summary_pdf.html'
#     context = {'tasks': tasks}
#     response = render(request, template_path, context)
#     pdf = open('task_summary.pdf', 'w')
#     pisa_status = pisa.CreatePDF(response.content, dest=pdf)
#     pdf.close()
#     if pisa_status.err:
#         return HttpResponse('Error generating PDF')
#     return redirect('task_summary')