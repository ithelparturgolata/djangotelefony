from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("telefony/", include("telefony.urls")),
    path("sms/", include("sms.urls")),
    path("task/", include("pracownik.urls")),
    path("splitter/", include("splitter.urls")),
    path("umowy/", include("umowy.urls")),
    path("rss/", include("rss.urls")),
    path("domofony/", include("domofony.urls")),
    path("it/", include("it.urls")),
]