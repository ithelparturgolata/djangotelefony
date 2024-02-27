from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from dashboard.views import register, login_view, logout_view, dashboard, dashboard_main


class ViewTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
	
	def test_login_view(self):
		url = reverse('login')
		request = self.factory.get(url)
		response = login_view(request)
		self.assertEqual(response.status_code, 200)
		
		# Test POST request
		request = self.factory.post(url, data={})
		request.session = {}
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
		response = login_view(request)
		self.assertEqual(response.status_code, 200)  # Assuming form is invalid
	
	def test_logout_view(self):
		url = reverse('logout')
		request = self.factory.get(url)
		response = logout_view(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('login'))
	
	