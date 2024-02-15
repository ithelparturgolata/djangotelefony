from django.shortcuts import render, redirect, get_object_or_404
from .models import Contractor, Contract
from .forms import ContractForm

def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_umowy')
    else:
        form = ContractForm()
    return render(request, 'add_contract.html', {'form': form})

def dashboard_umowy(request):
    contracts = Contract.objects.all()
    return render(request, 'dashboard-umowy.html', {'contracts': contracts})

def contract_details(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    return render(request, 'contract_details.html', {'contract': contract})
