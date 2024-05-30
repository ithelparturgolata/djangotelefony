from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from rss.views import (dashboard_przeciw, dashboard_przez, create_record, pdf,
                       search,  update_record, view_record, delete)


# testy urls
