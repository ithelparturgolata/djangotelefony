from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("dashboard_telefony", views.dashboard_telefony,
         name="dashboard_telefony"),
    path("dashboard_ce", views.dashboard_ce,
         name="dashboard_ce"),
    path("dashboard_nw", views.dashboard_nw,
         name="dashboard_nw"),
    path("dashboard_ns", views.dashboard_ns,
         name="dashboard_ns"),
    path("dashboard_lu", views.dashboard_lu,
         name="dashboard_lu"),
    path("dashboard_w", views.dashboard_w,
         name="dashboard_w"),
    path("create", views.create_record, name="create_telefony"),
    path("update/<int:pk>", views.update_record, name="update_telefony"),
    path("view/<int:pk>", views.view_record, name="view_telefony"),
    path("delete/<int:pk>", views.delete, name="delete_telefony"),
    path("sms/<int:pk>", views.sms_record, name="sms_telefony"),
    path("pdf", views.pdf, name="pdf_telefony"),
    path("raport_zmian", views.raport_zmian, name="raport_zmian"),
    path("search", views.search, name="search_telefony"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
