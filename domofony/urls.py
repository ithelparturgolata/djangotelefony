from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the task list view
    path('intercom/', views.dashboard_intercom, name='dashboard_intercom'),
    # URL pattern for adding a task
    path('intercom/add/', views.add_task_intercom, name='add_task_intercom'),
    # Add other URL patterns for your views here if needed
]
