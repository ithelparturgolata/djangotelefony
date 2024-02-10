from django.urls import path
from . import views

urlpatterns = [
    path('split-pdf/', views.split_pdf, name='pdf_splitter'),
]