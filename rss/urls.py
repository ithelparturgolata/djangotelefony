from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("", views.home, name=""),
    # path("register", views.register, name="register"),
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard_main", views.dashboard_main, name="dashboard_main"),
    path("dashboard_przeciw", views.dashboard_przeciw,
         name="dashboard-przeciw"),
    path("dashboard_przez", views.dashboard_przez,
         name="dashboard-przez"),
    path("create", views.create_record, name="create_rss"),
    path("update/<int:pk>", views.update_record, name="update_rss"),
    path("view/<int:pk>", views.view_record, name="view_rss"),
    path("delete/<int:pk>", views.delete, name="delete_rss"),
    path("sms/<int:pk>", views.sms_record, name="sms_rss"),
    path("pdf", views.pdf, name="pdf_rss"),
    path("sms", views.sms_historia, name="sms_historia"),
    path("search", views.search, name="search_rss"),
    path("view_file/<int:pk>", views.view_file, name="view_file"),
    path("upload_file/<int:pk>", views.upload_file, name="upload_file"),
    # path('download/<int:file_id>/', views.download_file, name='download_file'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
