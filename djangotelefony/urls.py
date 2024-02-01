from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("telefony/", include("telefony.urls")),
    path("sms/", include("sms.urls")),
    path("todo/", include("todo.urls")),
    # path("sms/", include("sms.urls")),
]