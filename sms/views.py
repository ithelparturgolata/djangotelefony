from sms.forms import SmsRecordFormSms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from telefony.models import Mieszkaniec, Blok
from smsapi.client import SmsApiPlClient
from django.core.paginator import Paginator
from django.contrib.auth.models import Group


@login_required(login_url="login")
def dashboard_sms(request):
    sms_group = Group.objects.get(name='sms_group')
    if request.user.groups.filter(name=sms_group).exists():
        my_records = Mieszkaniec.objects.all()
        p = Paginator(Mieszkaniec.objects.all(), 10)
        page = request.GET.get("page")
        my_record = p.get_page(page)
        return render(request, "dashboard-sms.html", {"records": my_records, "my_record": my_record})
    else:
        return render(request, 'error-sms.html')


def dashboard_sms_blok(request):
    my_records = Blok.objects.all()
    p = Paginator(Blok.objects.all(), 10)
    page = request.GET.get("page")
    my_record = p.get_page(page)
    
    return render(request, "dashboard-sms-blok.html",
                  {"records": my_records, "my_record": my_record})


def dashboard_sms_kontrahent(request):
    my_record = Mieszkaniec.objects.all().filter(zgoda__contains="tak")
    
    return render(request, "dashboard-sms-kontrahent.html", {"my_record": my_record})


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
            # my_records = Mieszkaniec.objects.all()
            p = Paginator(Mieszkaniec.objects.all(), 10)
            page = request.GET.get("page")
            my_record = p.get_page(page)
            
            return render(request, "dashboard-sms.html", {"form": form, "record": record, "my_record": my_record})
    
    context = {"form": form, "record": record, "my_record": my_record}
    return render(request, "sms-sms.html", context=context)


@login_required(login_url="login")
def sms_record_blok(request, pk):
    record = Blok.objects.get(id=pk)
    form = SmsRecordFormSms(instance=record)
    my_record = Blok.objects.get(id=pk)
    telefony_queryset = Mieszkaniec.objects.filter(zgoda='tak').filter(
        symbol_budynku=my_record.indeks_blok).values_list('telefon', flat=True)
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
            
            
            return render(request,
                          "dashboard-sms.html",
                          {"form": form,
                           "record": record, "my_record": my_record, "telefony_str": telefony_str})
    
    context = {"form": form, "record": record, "my_record": my_record, "telefony_str": telefony_str}
    return render(request, "sms-sms-blok.html", context=context)


@login_required(login_url="login")
def sms_ns_all(request):
    telefony_queryset = Mieszkaniec.objects.filter(
        zgoda='tak',
        administracja='NS'
    ).values_list('telefon', flat=True)
    
    telefony_str = ', '.join(map(str, telefony_queryset))
    
    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST)
        
        # Normalizacja treści SMS-a, usuwanie polskich znaków diakrytycznych
        to_remov = {
            "ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
            "ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
            "Ó": "O", "ó": "o", "Ń": "N", "ń": "n",
            "ć": "c", "Ć": "C", "Ż": "Z", "Ź": "Z",
            "ż": "z", "ź": "z", '„': "", '”': ""
        }
        for char in to_remov:
            content = content.replace(char, to_remov[char])
        
        # Wysłanie SMS-a przy użyciu SmsApiPlClient
        token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
        client = SmsApiPlClient(access_token=token)
        send_results = client.sms.send(
            to=phone,
            message=content,
            from_="SMBUDOWLANI"
        )
        
        # Pobranie wszystkich rekordów Mieszkaniec i paginacja
        my_records = Mieszkaniec.objects.all()
        p = Paginator(my_records, 10)
        page = request.GET.get("page")
        my_record = p.get_page(page)
        
        return render(request, "dashboard-sms.html", {
            "form": form,
            "my_record": my_record,
            "telefony_str": telefony_str
        })
    
    # Utworzenie pustego formularza, gdy metoda nie jest POST
    form = SmsRecordFormSms()
    context = {"form": form, "telefony_str": telefony_str}
    return render(request, "sms-sms-blok-ns-all.html", context=context)


@login_required(login_url="login")
def sms_nw_all(request):
    telefony_queryset = Mieszkaniec.objects.filter(
        zgoda='tak',
        administracja='NW'
    ).values_list('telefon', flat=True)
    
    telefony_str = ', '.join(map(str, telefony_queryset))
    
    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST)
        
        # Normalizacja treści SMS-a, usuwanie polskich znaków diakrytycznych
        to_remov = {
            "ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
            "ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
            "Ó": "O", "ó": "o", "Ń": "N", "ń": "n",
            "ć": "c", "Ć": "C", "Ż": "Z", "Ź": "Z",
            "ż": "z", "ź": "z", '„': "", '”': ""
        }
        for char in to_remov:
            content = content.replace(char, to_remov[char])
        
        # Wysłanie SMS-a przy użyciu SmsApiPlClient
        token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
        client = SmsApiPlClient(access_token=token)
        send_results = client.sms.send(
            to=phone,
            message=content,
            from_="SMBUDOWLANI"
        )
        
        # Pobranie wszystkich rekordów Mieszkaniec i paginacja
        my_records = Mieszkaniec.objects.all()
        p = Paginator(my_records, 10)
        page = request.GET.get("page")
        my_record = p.get_page(page)
        
        return render(request, "dashboard-sms.html", {
            "form": form,
            "my_record": my_record,
            "telefony_str": telefony_str
        })
    
    # Utworzenie pustego formularza, gdy metoda nie jest POST
    form = SmsRecordFormSms()
    context = {"form": form, "telefony_str": telefony_str}
    return render(request, "sms-sms-blok-nw-all.html", context=context)


@login_required(login_url="login")
def sms_ce_all(request):

    telefony_queryset = Mieszkaniec.objects.filter(
        zgoda='tak',
        administracja='CE'
    ).values_list('telefon', flat=True)


    telefony_str = ', '.join(map(str, telefony_queryset))

    if request.method == "POST":
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        form = SmsRecordFormSms(request.POST)

        # Normalizacja treści SMS-a, usuwanie polskich znaków diakrytycznych
        to_remov = {
            "ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
            "ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
            "Ó": "O", "ó": "o", "Ń": "N", "ń": "n",
            "ć": "c", "Ć": "C", "Ż": "Z", "Ź": "Z",
            "ż": "z", "ź": "z", '„': "", '”': ""
        }
        for char in to_remov:
            content = content.replace(char, to_remov[char])

        # Wysłanie SMS-a przy użyciu SmsApiPlClient
        token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
        client = SmsApiPlClient(access_token=token)
        send_results = client.sms.send(
            to=phone,
            message=content,
            from_="SMBUDOWLANI"
        )

        # Pobranie wszystkich rekordów Mieszkaniec i paginacja
        my_records = Mieszkaniec.objects.all()
        p = Paginator(my_records, 10)
        page = request.GET.get("page")
        my_record = p.get_page(page)

        return render(request, "dashboard-sms.html", {
            "form": form,
            "my_record": my_record,
            "telefony_str": telefony_str
        })

    # Utworzenie pustego formularza, gdy metoda nie jest POST
    form = SmsRecordFormSms()
    context = {"form": form, "telefony_str": telefony_str}
    return render(request, "sms-sms-blok-ce-all.html", context=context)


@login_required(login_url="login")
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched = searched.upper()
        
        my_records = (Mieszkaniec.objects.filter(nazwa__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(indeks__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
            adres__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
            telefon__contains=searched).filter(zgoda__contains="tak"))
        
        return render(request, "sms-search.html", {"searched": searched, "my_records": my_records})
    else:
        return render(request, "sms-search.html", {})


@login_required(login_url="login")
def search_blok(request):
    if request.method == "POST":
        searched = request.POST.get("searched", "").strip()
        searched_upper = searched.upper()
        my_records = Blok.objects.filter(
            adres_blok__icontains=searched_upper
        ) | Blok.objects.filter(
            indeks_blok__icontains=searched_upper
        )
        
        return render(request, "sms-search-blok.html",
                      {"searched": searched, "my_records": my_records})
    else:
        return render(request, "sms-search-blok.html", {})


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


@login_required(login_url="login")
def sms_checked(request):
    if request.method == "POST":
        if "checked_numbers" in request.POST:
            checked_numbers = request.POST.get("checked_numbers", "").split(',')
            form = SmsRecordFormSms()
            
            context = {
                "form": form,
                "checked_numbers": checked_numbers,
            }
            return render(request, "sms-sms-checked.html", context)
        else:
            phone = request.POST.get("phone")
            content = request.POST.get("content")
            form = SmsRecordFormSms(request.POST)
            
            to_remov = {
                "ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
                "ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
                "Ó": "O", "ó": "o", "Ń": "N", "ń": "n",
                "ć": "c", "Ć": "C", "Ż": "Z", "Ź": "Z",
                "ż": "z", "ź": "z", '„': "", '”': ""
            }
            for char in to_remov:
                content = content.replace(char, to_remov[char])
            
            token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
            client = SmsApiPlClient(access_token=token)
            send_results = []
            for number in phone.split(','):
                send_results.append(client.sms.send(
                    to=number.strip(),
                    message=content,
                    from_="SMBUDOWLANI"
                ))
            
            context = {
                "form": form,
                "send_results": send_results,
            }
            return render(request, "sms-sms-checked.html", context)
    
    return redirect('dashboard_sms')
