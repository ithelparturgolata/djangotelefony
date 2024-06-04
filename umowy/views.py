from django.shortcuts import render, redirect, get_object_or_404
from .models import Contractor, Contract, ContractFile, ContractFileAnnex
from .forms import ContractForm, ContractFileForm, ContractorForm, ContractFileFormAnnex
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.paginator import Paginator


def add_contract(request):
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
    contracts = Contract.objects.all()
    if request.method == 'POST':
        form = ContractorForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            existing_contractor = Contractor.objects.filter(name__iexact=name).exists()
            if existing_contractor:
                messages.error(request, f"Wykonawca '{name}' już jest w bazie.")
            else:
                form.save()
                return redirect('dashboard_contracts')
        else:
            messages.error(request, "Błędy w formularzu.")  # Display form errors
    else:
        form = ContractorForm()
    return render(request, 'add-contractor.html', {'form': form, 'contracts': contracts})


@login_required(login_url="login")
def dashboard_contracts(request):
    umowy_group = Group.objects.get(name='umowy_group')
    if request.user.groups.filter(name=umowy_group).exists():
        contracts = Contract.objects.all()
        p = Paginator(Contract.objects.all(), 10)
        page = request.GET.get("page")
        contracts = p.get_page(page)
        return render(request, 'dashboard-contracts.html', {'contracts': contracts})
    else:
        return render(request, 'error-contracts.html', {'message': ''})


@login_required(login_url="login")
def details_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    my_files = ContractFile.objects.filter(contract=contract)
    annex_files = ContractFileAnnex.objects.filter(contract=contract)
    
    if request.method == 'POST':
        form = ContractFileForm(request.POST, request.FILES)
        annex_form = ContractFileFormAnnex(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = contract
            instance.save()
            return redirect('details_contract', contract_id=contract_id)
        elif annex_form.is_valid():
            instance_annex = annex_form.save(commit=False)
            instance_annex.contract = contract
            instance_annex.save()
            return redirect('details_contract', contract_id=contract_id)
    else:
        form = ContractFileForm()
        annex_form = ContractFileFormAnnex()
    
    return render(request, 'details-contract.html',
                  {'contract': contract, 'form': form, 'annex_form': annex_form, 'my_files': my_files,
                   'annex_files': annex_files})


@login_required(login_url="login")
def upload_file_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.contract = contract
            file.save()
            return redirect('details_contract', contract_id=contract.id)
        else:
            messages.error(request, "Only PDF files are allowed.")
    else:
        form = ContractFileForm()
    return render(request, 'file-upload-contract.html', {'form': form, 'contract': contract})


@login_required(login_url="login")
def upload_file_contract_annex(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractFileFormAnnex(request.POST, request.FILES)
        if form.is_valid():
            file_annex = form.save(commit=False)
            file_annex.contract = contract
            file_annex.save()
            return redirect('details_contract', contract_id=contract.id)
        else:
            raise ValidationError("Błędy w formularzu")  # Raise validation error if form is not valid
    else:
        form = ContractFileFormAnnex()
    return render(request, 'file-upload-contract-annex.html', {'form': form, 'contract': contract})


@login_required(login_url="login")
def search_contracts(request):
    searched = request.POST.get("searched", "").lower()
    my_contracts = Contract.objects.filter(contractor__name__icontains=searched)

    if not my_contracts:
        message = f"<b> Nie znaleziono Wykonawcy '{searched}'.</b>"
    else:
        message = ""

    return render(request, "search-contract.html", {"searched": searched, "my_contracts": my_contracts,
                                                    "message": message})
