from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_contract, name='add_contract'),
    path('dashboard_umowy/', views.dashboard_umowy, name='dashboard_umowy'),
    path('details/<int:contract_id>/', views.contract_details, name='contract_details'),
]
