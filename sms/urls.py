from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("dashboard_sms", views.dashboard_sms,
         name="dashboard_sms"),
    path("dashboard_sms_kontrahent", views.dashboard_sms_kontrahent,
         name="dashboard-sms-kontrahent"),
    path("dashboard_sms_blok", views.dashboard_sms_blok,
         name="dashboard-sms-blok"),
    path("dashboard_sms_lu", views.dashboard_sms_lu,
         name="dashboard-sms-lu"),
    path("dashboard_szablony", views.dashboard_szablony,
         name="dashboard-szablony"),
    path("view/<int:pk>", views.view_record_sms, name="sms-view"),
    path("view_blok/<int:pk>", views.view_record_sms_blok, name="sms-view-blok"),
    path("view_lu/<int:pk>", views.view_record_sms_lu, name="sms-view-lu"),
    path("sms/<int:pk>", views.sms_record, name="sms-sms"),
    path("sms_blok/<int:pk>", views.sms_record_blok, name="sms-sms-blok"),
    path("sms_lu", views.sms_record_lu, name="sms-sms-lu"),
    path("sms_test", views.sms_test, name="sms-test"),
    path("search", views.search, name="search-sms"),
    path("search_kontrahent", views.search_kontrahent, name="search-sms-kontrahent"),
    path("search_blok", views.search_blok, name="search-sms-blok"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
