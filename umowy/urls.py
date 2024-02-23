from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add/', views.add_contract, name='add_contract'),
    path('add_contractor/', views.add_contractor, name='add_contractor'),
    path('dashboard_umowy/', views.dashboard_contracts, name='dashboard_contracts'),
    path('details/<int:contract_id>/', views.details_contract, name='details_contract'),
    path('search/', views.search_contracts, name='search_contracts'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
