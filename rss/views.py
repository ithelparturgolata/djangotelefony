from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import CreateUserForm, LoginForm, \
    AddRecordForm, UpdateRecordForm, SmsRecordForm, RecordFileForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .functions import handle_uploaded_file
from .models import Record
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
from datetime import date, datetime

@login_required(login_url="login")
def dashboard_main(request):
    my_records = Record.objects.all()
    p = Paginator(Record.objects.all(), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)

    return render(request, "dashboard-main.html",
                  {"records": my_records, "my_record": my_record})


@login_required(login_url="login")
def dashboard_przeciw(request):
    my_records = Record.objects.all()
    p = Paginator(Record.objects.all(), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)

    return render(request, "dashboard-przeciw.html",
                  {"records": my_records, "my_record": my_record})


@login_required(login_url="login")
def dashboard_przez(request):
    my_records = Record.objects.all()
    p = Paginator(Record.objects.all(), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)

    return render(request, "dashboard-przez.html",
                  {"records": my_records, "my_record": my_record})


# add pozew
@login_required(login_url="login")
def create_record(request):
    form = AddRecordForm()
    if request.method == "POST":

        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dodano pozew")
            return redirect("dashboard_main")
    context = {"form": form}
    return render(request, "create-record.html", context=context)


# update pozew
@login_required(login_url="login")
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    all_records = Record.objects.get(id=pk)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Zaktualizowano pozew")
            return redirect("dashboard_main")

    # context = {"form": form}
    return render(request, "update-record.html",
                  {"form": form, "record": record, "all_records": all_records})


# view pozew
@login_required(login_url="login")
def view_record(request,  pk):
    all_records = Record.objects.get(id=pk)
    context = {"record": all_records}

    return render(request, "view-record.html", context=context)


# delete pozew
@login_required(login_url="login")
def delete(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Skasowano pozew")
    return redirect("dashboard_main")


# sms pozew
@login_required(login_url="login")
def sms_record(request,  pk):
    record = Record.objects.get(id=pk)
    form = SmsRecordForm(instance=record)
    my_record = Record.objects.get(id=pk)

    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordForm(request.POST, instance=record)
        to_remov = {"ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
                    "ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
                    "Ó": "O", "ó": "o",
                    "Ń": "N", "ń": "n", "ć": "c", "Ć": "C",
                    "Ż": "Z", "Ź": "Z", "ż": "z", "ź": "z",
                    '„': "", '”': ""}
        for char in to_remov.keys():
            content = content.replace(char, to_remov[char])
        if request.method == "POST":
            token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
            client = SmsApiPlClient(access_token=token)
            send_results = client.sms.send(to=phone,
                                           message=content,
                                           from_="SMBUDOWLANI")
            my_records = Record.objects.all()
            p = Paginator(Record.objects.all(), 10)
            page = request.GET.get("page")
            my_record = p.get_page(page)

            now = datetime.now()
            today = str(date.today())
            hour = now.strftime("%H:%M:%S")
            user = auth.get_user(request)
            file = open("save/sms/sms_rss.txt", "a+")
            file.write("Odbiorca = " + phone + "\n" +
                       "Tresc = " + content + "\n" +
                       "Data:" + today + "\n" +
                       "Wyslal = " + str(user) +
                       "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
            file.close

            return render(request,
                          "dashboard-main.html",
                          {"form": form,
                           "record": record, "my_record": my_record})

    context = {"form": form, "record": record, "my_record": my_record}
    return render(request, "sms-record.html", context=context)


# pdf pozew
@login_required(login_url="login")
def pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    records = Record.objects.all()
    lines = []

    for record in records:
        lines.append(record.powod)
        lines.append(record.dotyczy)
        lines.append(record.wyrok1)
        lines.append(record.wyrok2)
        lines.append(record.egzekucja)
        lines.append(record.uwagi)
        lines.append(record.zakonczenie)
        lines.append(record.status)
        lines.append("#######################################")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="raport.pdf")


@login_required(login_url="login")
def sms_historia(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    records = open('save/sms/sms_rss.txt', 'r')
    lines = []

    for record in records:
        lines.append(record)

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="raport_sms.pdf")


# search pozew
@login_required(login_url="login")
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        my_records = Record.objects.filter(powod__contains=searched)

        return render(request, "dashboard-search.html",
                      {"searched": searched, "my_records": my_records})
    else:
        return render(request, "dashboard-search.html", {})


# view pozew pliki
@login_required(login_url="login")
def view_file(request, pk):
    my_record = Record.objects.get(id=pk)
    context = {"record": my_record}

    return render(request, "view-file.html", context=context)


# upload pozew pliki
@login_required(login_url="login")
def upload_file(request, pk):
    """
    View function allowing uploading a file to a specific contract.

    Fetches a contract with a specified identifier from the database. If the request method is POST,
    processes the form submission to upload a file to the contract. Otherwise, renders the file upload
    form to the contract.

    Args:
    request (HttpRequest): HTTP request object.
    pk (int): Identifier of the contract for which the file should be uploaded.

    Returns:
    HttpResponse: Renders the "file_upload_contract.html" template with the file upload form and
    contract information.
    """
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.record = record
            file.save()
            return redirect('view_file', pk=record.id)
    else:
        form = RecordFileForm()
    return render(request, 'upload-file.html', {'form': form, 'record': record})

# @login_required(login_url="login")
# def upload_file(request, pk):
#     record = Record.objects.get(id=pk)
#     form = UploadFileForm(instance=record)
#     my_record = Record.objects.get(id=pk)
#
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES, instance=record)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Dodano plik")
#             return redirect('view_file', pk)
#     else:
#         form = UploadFileForm()
#     context = {"form": form, "record": record, "my_record": my_record}
#     return render(request, 'upload-file.html', context=context)