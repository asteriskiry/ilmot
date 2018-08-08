from django.urls import reverse
from django.urls import resolve
from django.test import TestCase

from .views import home

class HomeTests(TestCase):
    def test_event_add_view_status_code(self):
        url = 'http://127.0.0.1:8000/eventsignup/event/add/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_add_sitsit_view_status_code(self):
        url = 'http://127.0.0.1:8000/eventsignup/event/add/sitsit/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
