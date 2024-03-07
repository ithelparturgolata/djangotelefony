from django.shortcuts import render, redirect, get_object_or_404
from .models import Contractor, Contract, ContractFile
from .forms import ContractForm, ContractFileForm, ContractorForm, ContractsSearchForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


def add_contract(request):
    """
    View to add a new contract.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for adding a new contract.
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
    View to add a new contractor.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template for adding a new contractor.
    """
    if request.method == 'POST':
        form = ContractorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_contracts')
        else:
            raise ValidationError("Błędy w formularzu")  # Raise validation error if form is not valid
    else:
        form = ContractorForm()
    return render(request, 'add-contractor.html', {'form': form})


@login_required(login_url="login")
def dashboard_contracts(request):
    """
    View to display all contracts.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template displaying all contracts.
    """
    contracts = Contract.objects.all()
    return render(request, 'dashboard-contracts.html', {'contracts': contracts})


@login_required(login_url="login")
def details_contract(request, contract_id):
    """
    View to display details of a specific contract.

    Args:
    - request (HttpRequest): The HTTP request object.
    - contract_id (int): The ID of the contract.

    Returns:
    - HttpResponse: Rendered template displaying details of the contract.
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
            raise ValidationError("Błędy w formularzu")  # Raise validation error if form is not valid
    else:
        form = ContractFileForm()
    return render(request, 'details-contract.html', {'contract': contract, 'form': form, 'my_files': my_files})


@login_required(login_url="login")
def upload_file_contract(request, contract_id):
    """
    View to upload a file for a specific contract.

    Args:
    - request (HttpRequest): The HTTP request object.
    - contract_id (int): The ID of the contract.

    Returns:
    - HttpResponse: Rendered template for uploading a file for the contract.
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
            raise ValidationError("Błędy w formularzu")  # Raise validation error if form is not valid
    else:
        form = ContractFileForm()
    return render(request, 'file_upload_contract.html', {'form': form, 'contract': contract})


@login_required(login_url="login")
def search_contracts(request):
    """
    View to search for contracts by contractor name.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered template displaying search results.
    """
    searched = request.POST.get("searched", "").lower()
    my_contracts = Contract.objects.filter(contractor__name__icontains=searched)

    if not my_contracts:
        message = f"<b> Nie znaleziono Wykonawcy '{searched}'.</b>"
    else:
        message = ""

    return render(request, "search-contract.html", {"searched": searched, "my_contracts": my_contracts, "message": message})
