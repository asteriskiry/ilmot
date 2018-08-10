from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from .models import EventType, EventOwner, Events, Participant, Sitz, Annualfest, Excursion, OtherEvent
from .forms import SitzForm
#ehkä luo uusi superuser myös?
#EI TOIMI ATM, EI AJA KÄSKSYLLÄ TEST MTN FILUJA
class EventsSignupSitzTests(TestCase):
    def setUp(self):
        #EventType.objects.create(event_type='sitsit')
        User.objects.create_user(username='test', email='john@doe.co', password='123')
    def test_new_sitz_form_send(self):
        url = 'http://127.0.0.1:8000/eventsignup/event/add/sitsit'
        EventType.objects.create(event_type='sitz')
        EventType.objects.create(event_type='sitsit')
        EventOwner.objects.create(name='test')
        data = {
        'name':'lol',
        'place':'qtalo',
        'date':'2018-01-01',
        'start_time':'00.00.00',
        'description':'kuvaus',
        'signup_starts':'2018-02-02',
        'signup_ends':'2018-03-03'
        }
        response = self.client.post(url, data)
        self.assertTrue(EventType.objects.exists())

    def test_contains_form(self):
        url = 'http://127.0.0.1:8000/eventsignup/event/add/sitsit'
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, SitzForm)

    def test_csrf(self):
        url = 'http://127.0.0.1:8000/eventsignup/event/add/sitsit'
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
