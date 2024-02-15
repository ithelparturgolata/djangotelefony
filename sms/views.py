from requests import auth
from sms.forms import SmsRecordFormSms, SmsRecordFormSmsBlok
from django.shortcuts import render
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

from telefony.models import Mieszkaniec, Blok
from smsapi.client import SmsApiPlClient
from django.core.paginator import Paginator
from datetime import date, datetime

@login_required(login_url="login")
def dashboard_sms(request):
    my_records = Mieszkaniec.objects.all()
    p = Paginator(Mieszkaniec.objects.all(), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)

    return render(request, "dashboard-sms.html",
                  {"records": my_records, "my_record": my_record})


def dashboard_sms_blok(request):
    my_records = Blok.objects.all()
    p = Paginator(Blok.objects.all(), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)

    return render(request, "dashboard-sms-blok.html",
                  {"records": my_records, "my_record": my_record})


def dashboard_sms_kontrahent(request):
    my_records = Mieszkaniec.objects.filter(zgoda__contains="tak")
    p = Paginator(Mieszkaniec.objects.all().filter(zgoda__contains="tak"), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)

    return render(request, "dashboard-sms-kontrahent.html",
                  {"records": my_records, "my_record": my_record})


def dashboard_sms_lu(request):
    my_records_lu = Mieszkaniec.objects.all().filter(administracja__contains="LU")
    p = Paginator(Mieszkaniec.objects.all().filter(zgoda__contains="tak"), 10)
    page = request.GET.get("page")
    my_record_lu = p.get_page(page)

    return render(request, "dashboard-sms-lu.html",
                  {"records": my_records_lu, "my_record": my_record_lu})




# @login_required(login_url="login")
# def dashboard_nw_sms_blok(request):
#     my_records = Blok.objects.all().filter(administracja="nw")
#     p = Paginator(Blok.objects.all().filter(administracja="nw"), 10)
#     page = request.GET.get("page")
#     my_record = p.get_page(page)
#
#     return render(request, "dashboard-nw-sms-blok.html",
#                   {"records": my_records, "my_record": my_record})


# view pozew
@login_required(login_url="login")
def view_record_sms(request, pk):
    all_records = Mieszkaniec.objects.get(id=pk)
    context = {"record": all_records}

    return render(request, "sms-view.html", context=context)


@login_required(login_url="login")
def view_record_sms_blok(request, pk):
    my_records_blok = Blok.objects.get(id=pk)
    context = {"my_records_blok": my_records_blok}
    
    return render(request, "sms-view-blok.html", context=context)


@login_required(login_url="login")
def view_record_sms_lu(request, pk):
    all_records = Mieszkaniec.objects.get(id=pk)
    context = {"record": all_records}

    return render(request, "sms-view-lu.html", context=context)


# sms pozew
@login_required(login_url="login")
def sms_record(request, pk):
    record = Mieszkaniec.objects.get(id=pk)
    form = SmsRecordFormSms(instance=record)
    my_record = Mieszkaniec.objects.get(id=pk)

    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST, instance=record)
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
            my_records = Mieszkaniec.objects.all()
            p = Paginator(Mieszkaniec.objects.all(), 10)
            page = request.GET.get("page")
            my_record = p.get_page(page)

            # now = datetime.now()
            # today = str(date.today())
            # hour = now.strftime("%H:%M:%S")
            # user = auth.get_user(request)
            # file = open("save/sms/sms_kontrahent.txt", "a+")
            # file.write("Odbiorca = " + phone + "\n" +
            #            "Tresc = " + content + "\n" +
            #            "Data:" + today + "\n" +
            #            "Wyslal = " + str(user) +
            #            "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
            # file.close

            return render(request,
                          "dashboard-sms.html",
                          {"form": form,
                           "record": record, "my_record": my_record})

    context = {"form": form, "record": record, "my_record": my_record}
    return render(request, "sms-sms.html", context=context)



@login_required(login_url="login")
def sms_record_blok(request, pk):
    record = Blok.objects.get(id=pk)
    form = SmsRecordFormSms(instance=record)
    my_record = Blok.objects.get(id=pk)
    telefony_queryset = Mieszkaniec.objects.filter(zgoda='tak').filter(symbol_budynku=my_record.indeks_blok).values_list('telefon', flat=True)
    telefony_str = ', '.join(map(str, telefony_queryset))
    
    
    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST, instance=record)
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
            my_records = Mieszkaniec.objects.all()
            p = Paginator(Mieszkaniec.objects.all(), 10)
            page = request.GET.get("page")
            my_record = p.get_page(page)
            
            # now = datetime.now()
            # today = str(date.today())
            # hour = now.strftime("%H:%M:%S")
            # user = auth.get_user(request)
            # file = open("save/sms/sms_blok.txt", "a+")
            # file.write("Odbiorca = " + phone + "\n" +
            #            "Tresc = " + content + "\n" +
            #            "Data:" + today + "\n" +
            #            "Wyslal = " + str(user) +
            #            "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
            # file.close
            
            return render(request,
                          "dashboard-sms.html",
                          {"form": form,
                           "record": record, "my_record": my_record, "telefony_str": telefony_str})
    
    context = {"form": form, "record": record, "my_record": my_record, "telefony_str": telefony_str}
    return render(request, "sms-sms-blok.html", context=context)


@login_required(login_url="login")
def sms_record_lu(request):
    record_lu = Mieszkaniec.objects.all()
    form = SmsRecordFormSms(instance=record_lu)
    my_record_lu = Mieszkaniec.objects.all().filter(zgoda__contains="tak") | Mieszkaniec.objects.all().filter(administracja__contains="LU")
    telefony_queryset = Mieszkaniec.objects.filter(zgoda='tak').filter(
        symbol_budynku=my_record_lu.administracja).values_list('telefon', flat=True)
    telefony_str = ', '.join(map(str, telefony_queryset))
    
    
    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST, instance=record_lu)
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
            my_records = Mieszkaniec.objects.all()
            p = Paginator(Mieszkaniec.objects.all(), 10)
            page = request.GET.get("page")
            my_record = p.get_page(page)
            
            # now = datetime.now()
            # today = str(date.today())
            # hour = now.strftime("%H:%M:%S")
            # user = auth.get_user(request)
            # file = open("save/sms/sms_blok.txt", "a+")
            # file.write("Odbiorca = " + phone + "\n" +
            #            "Tresc = " + content + "\n" +
            #            "Data:" + today + "\n" +
            #            "Wyslal = " + str(user) +
            #            "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
            # file.close
            
            return render(request,
                          "dashboard-sms.html",
                          {"form": form,
                           "record_lu": record_lu, "my_record": my_record, "telefony_str": telefony_str})
    
    context = {"form": form, "record_lu": record_lu, "my_record_lu": my_record_lu, "telefony_str": telefony_str}
    return render(request, "sms-sms-lu.html", context=context)




# search pozew
@login_required(login_url="login")
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        my_records = Mieszkaniec.objects.filter(nazwa__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
            indeks__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(adres__contains=searched).filter(zgoda__contains="tak")
        return render(request, "sms-search.html",
                      {"searched": searched, "my_records": my_records})
    else:
        return render(request, "sms-search.html", {})


@login_required(login_url="login")
def search_kontrahent(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        my_records = Mieszkaniec.objects.filter(nazwa__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
            indeks__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(adres__contains=searched).filter(zgoda__contains="tak")
        return render(request, "sms-search-kontrahent.html",
                      {"searched": searched, "my_records": my_records})
    else:
        return render(request, "sms-search-kontrahent.html", {})


@login_required(login_url="login")
def search_blok(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        my_record = Blok.objects.filter(indeks_blok__contains=searched) | Blok.objects.filter(
            adres_blok__contains=searched)
        return render(request, "sms-search-blok.html",
                      {"searched": searched, "my_records": my_record})
    else:
        return render(request, "sms-search-blok.html", {})



@login_required(login_url="login")
def dashboard_szablony(request):

    return render(request, "dashboard_szablony.html")


@login_required(login_url="login")
def sms_test(request):
    record = Mieszkaniec.objects.all()
    form = SmsRecordFormSms()
    my_record = Mieszkaniec.objects.all()

    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST)
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
            my_records = Mieszkaniec.objects.all()
           

            return render(request,
                          "dashboard-sms.html",
                          {"form": form,
                           "record": record, "my_record": my_record})

    context = {"form": form, "record": record, "my_record": my_record}
    return render(request, "sms-sms.html", context=context)
