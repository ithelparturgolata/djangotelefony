from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from dashboard.views import register, login_view, logout_view, dashboard, dashboard_main


