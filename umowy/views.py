"""Opis modułu"""

__name__ = "umowy_module"
__author__ = "Artur Gołata"
__license__ = "MIT"
__version__ = "1.0"
__status__ = "production"

from django.shortcuts import render, redirect, get_object_or_404
from .models import Contractor, Contract, ContractFile
from .forms import ContractForm, ContractFileForm, ContractorForm, ContractsSearchForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def add_contract(request):
    """
    Sposób dodania umowy.
    
    Jeśli metodą żądania jest POST, sprawdza dane w formularzu dodania umowy.
    Jeśli formularz jest prawidłowy, zapisuje umowę i przekierowuje do dashboardu umów.
    Jeśli metodą żądania nie jest POST, renderowany jest szablon add-contract.html
    z pustym formularzem dodania umowy.
    
    Parametry:
    - żądanie (HttpRequest): Obiekt żądania HTTP.
    
    Zwroty:
    - HttpResponse: Odpowiedź HTTP z wyrenderowanym szablonem.
    """
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_contracts')
    else:
        form = ContractForm()
    return render(request, 'add-contract.html', {'form': form})


@login_required(login_url="login")
def add_contractor(request):
    """
    Funkcja podglądu umożliwiająca dodanie nowego wykonawcy.
    
    Jeśli metodą żądania jest POST, przetwarza dane z formularza przesłane przez użytkownika.
    Jeżeli dane w formularzu są prawidłowe, zapisuje wykonawcę do bazy danych.
    Następnie przekierowuje użytkownika na stronę dashboardu umów.
    
    Jeśli metodą żądania jest GET, wyświetla użytkownikowi formularz dodania wykonawcy.
    
    Argumenty:
     żądanie (HttpRequest): Obiekt żądania HTTP.
    
    Zwroty:
     HttpResponse: Jeśli metodą żądania jest POST i dane formularza są prawidłowe,
         przekierowuje użytkownika na stronę dashboardu umów.
         Jeśli metodą żądania jest GET, wyświetla użytkownikowi formularz dodania wykonawcy.
    """
    if request.method == 'POST':
        form = ContractorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_contracts')
    else:
        form = ContractorForm()
    return render(request, 'add-contract.html', {'form': form})


@login_required(login_url="login")
def dashboard_contracts(request):
    """
    Funkcja View umożliwiająca wyświetlenie wszystkich umów w tabeli.
    
    Pobiera wszystkie umowy z bazy danych i przekazuje je do szablonu w celu renderowania.
    
    Argumenty:
     żądanie (HttpRequest): Obiekt żądania HTTP.
    
    Zwroty:
     HttpResponse: Renderuje szablon „dashboard-contracts.html” z listą umów.
    
    """
    contracts = Contract.objects.all()
    return render(request, 'dashboard-contracts.html', {'contracts': contracts})


@login_required(login_url="login")
def details_contract(request, contract_id):
    """
    Funkcja przeglądania służąca do wyświetlania szczegółów umowy i dodawania plików do umowy.
    
    Pobiera umowę o określonym identyfikatorze z bazy danych. Pobiera również wszystkie powiązane pliki
    z umową. Jeśli metodą żądania jest POST, przetwarza przesłanie formularza w celu dodania nowego pliku umowy.
    W przeciwnym razie renderuje stronę ze szczegółami umowy zawierającą informacje o umowie i formularz dla
    dodawanie plików.
    
    Argumenty:
     Żądanie (HttpRequest): Obiekt żądania HTTP.
     umowa_id (int): Identyfikator umowy, dla którego mają zostać wyświetlone szczegóły.
    
    Zwroty:
     HttpResponse: Renderuje szablon „details-contract.html” ze szczegółami umowy i formularzem dodania pliku.
    
    """
    contract = get_object_or_404(Contract, pk=contract_id)
    my_files = ContractFile.objects.filter(contract=contract)
    if request.method == 'POST':
        form = ContractFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = contract
            instance.save()
            return redirect('details_contract', contract_id=contract_id)
    else:
        form = ContractFileForm()
    return render(request, 'details-contract.html', {'contract': contract, 'form': form, 'my_files': my_files})


@login_required(login_url="login")
def upload_file_contract(request, contract_id):
    """
    Funkcja przeglądania umożliwiająca przesłanie pliku do konkretnej umowy.
    
    Pobiera umowę o określonym identyfikatorze z bazy danych. Jeśli metodą żądania jest POST,
    przetwarza wypełnienie formularza w celu przesłania pliku do umowy. W przeciwnym razie renderuje przesyłanie pliku
    formularz do umowy.
    
    Argumenty:
     żądanie (HttpRequest): Obiekt żądania HTTP.
     umowa_id (int): Identyfikator umowy, dla którego ma zostać przesłany plik.
    
    Zwroty:
     HttpResponse: Renderuje szablon „file_upload_contract.html” z formularzem przesyłania pliku i
     informacje o umowie.
    
    """
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.contract = contract
            file.save()
            return redirect('details_contract', contract_id=contract.id)
    else:
        form = ContractFileForm()
    return render(request, 'file_upload_contract.html', {'form': form, 'contract': contract})


@login_required(login_url="login")
def search_contracts(request):
    """
     Funkcja przeglądania pozwalająca na wyszukiwanie umów po nazwie wykonawcy.
    
     Pobiera szukane słowo kluczowe z żądania POST, konwertuje je na małe litery,
     i filtruje umowy po nazwie wykonawcy zawierającej szukane słowo kluczowe.
     W przypadku braku wykoknawcy generuje komunikat informujący, że nie odnaleziono żadnego wykonawcy.
     Renderuje szablon „search-contract.html” z wynikami wyszukiwania i komunikatem.
    
     Argumenty:
         request (HttpRequest): Obiekt żądania HTTP zawierający wyszukiwane słowo kluczowe.
    
     Zwroty:
         HttpResponse: Renderuje szablon „search-contract.html” z wynikami wyszukiwania,
         wyszukiwane słowo kluczowe i wiadomość.
        
     """
    searched = request.POST.get("searched", "").lower()
    my_contracts = Contract.objects.filter(contractor__name__icontains=searched)

    if not my_contracts:
        message = f"<b> Nie znaleziono Wykonawcy '{searched}'.</b>"
    else:
        message = ""

    return render(request, "search-contract.html", {"searched": searched, "my_contracts": my_contracts, "message": message})


