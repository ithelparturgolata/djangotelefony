from django.shortcuts import render, redirect, get_object_or_404
from .models import Contractor, Contract, ContractFile
from .forms import ContractForm, ContractFileForm, ContractorForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_umowy')
    else:
        form = ContractForm()
    return render(request, 'add-contract.html', {'form': form})


@login_required(login_url="login")
def add_contractor(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save()
            # Update status based on days left until the end of the contract
            contract.update_status()
            return redirect('dashboard_umowy')
    else:
        form = ContractForm()
    return render(request, 'add-contract.html', {'form': form})


@login_required(login_url="login")
def dashboard_umowy(request):
    contracts = Contract.objects.all()
    return render(request, 'dashboard-umowy.html', {'contracts': contracts})


@login_required(login_url="login")
def contract_details(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    my_files = ContractFile.objects.filter(contract=contract)
    if request.method == 'POST':
        form = ContractFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = contract
            instance.save()
            return redirect('contract_details', contract_id=contract_id)
    else:
        form = ContractFileForm()
    return render(request, 'contract-details.html', {'contract': contract, 'form': form, 'my_files': my_files})


@login_required(login_url="login")
def contract_file_upload(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.contract = contract
            file.save()
            return redirect('contract_details', contract_id=contract.id)
    else:
        form = ContractFileForm()
    return render(request, 'contract_file_upload.html', {'form': form, 'contract': contract})


@login_required(login_url="login")
def search_umowy(request):
    searched = request.POST.get("searched", "").lower()
    my_contracts = Contract.objects.filter(contractor__name__icontains=searched)

    if not my_contracts:
        message = f"<b> Nie znaleziono Wykonawcy '{searched}'.</b>"
    else:
        message = ""

    return render(request, "umowy-search.html", {"searched": searched, "my_contracts": my_contracts, "message": message})


