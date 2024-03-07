from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('task/home', views.home, name='home'),
    path('add_task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path("dashboard_todo", views.dashboard_task, name='dashboard_task'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
