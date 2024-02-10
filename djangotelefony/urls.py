from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("telefony/", include("telefony.urls")),
    path("sms/", include("sms.urls")),
    path("pracownik/", include("pracownik.urls")),
    path("splitter/", include("splitter.urls")),
]