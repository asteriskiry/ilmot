from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from django.contrib.auth.models import User
from .models import EventType, EventOwner, Events, Participant, Sitz, Annualfest, Excursion, OtherEvent
from .forms import SitzForm, AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm

#Custom  uupuu, sil ei oo omaa modelia, se tehdään ehkä jossai vaihees?


class EventsSignupExcursionTests(TestCase):
    def setUp(self):
        #EventType.objects.create(event_type='sitsit')
        User.objects.create_user(username='test', email='lol@example.com', password='123')
        EventType.objects.create(event_type='ekskursio')
        EventOwner.objects.create(name='test')
        self.client.login(username='test', password='123')

    def test_excursion_view_status_code(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/ekskursio'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_form(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/ekskursio'
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, ExcursionForm)

    def test_csrf(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/ekskursio'
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_excursion_form_send(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/ekskursio'
        data = {
        'name':'lol',
        'place':'qtalo',
        'date':'2018-01-01',
        'end_date':'2018-01-02',
        'start_time':'00.00.00',
        'description':'kuvaus',
        'signup_starts':'2018-02-02',
        'signup_ends':'2018-03-03'
        }
        response = self.client.post(url, data)
        self.assertTrue(EventType.objects.exists())

    def test_excursion_form_invalid_form_data(self):
        #Invalid post data should not redirect
        #The expected behavior is to show the form again with validation errors
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/ekskursio'
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

class EventsSignupAnnualfestTests(TestCase):
    def setUp(self):
        #EventType.objects.create(event_type='sitsit')
        User.objects.create_user(username='test', email='lol@example.com', password='123')
        EventType.objects.create(event_type='vuosijuhlat')
        EventOwner.objects.create(name='test')
        self.client.login(username='test', password='123')

    def test_annualfest_view_status_code(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/vuosijuhlat'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_form(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/vuosijuhlat'
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, AnnualfestForm)

    def test_csrf(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/vuosijuhlat'
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_annualfest_form_send(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/vuosijuhlat'
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

    def test_annualfest_form_invalid_form_data(self):
        #Invalid post data should not redirect
        #The expected behavior is to show the form again with validation errors
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/vuosijuhlat'
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class EventsSignupSitzTests(TestCase):
    def setUp(self):
        #EventType.objects.create(event_type='sitsit')
        User.objects.create_user(username='test', email='lol@example.com', password='123')
        EventType.objects.create(event_type='sitsit')
        EventOwner.objects.create(name='test')
        self.client.login(username='test', password='123')

    def test_sitsit_view_status_code(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/sitsit'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_form(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/sitsit'
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, SitzForm)

    def test_csrf(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/sitsit'
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_sitz_form_send(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/sitsit'
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

    def test_sitz_form_invalid_form_data(self):
        #Invalid post data should not redirect
        #The expected behavior is to show the form again with validation errors
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/sitsit'
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

class EventsSignupOtherEventTests(TestCase):
    def setUp(self):
        #EventType.objects.create(event_type='sitsit')
        User.objects.create_user(username='test', email='lol@example.com', password='123')
        EventType.objects.create(event_type='muutapahtuma')
        EventType.objects.create(event_type='muu')
        EventOwner.objects.create(name='test')
        self.client.login(username='test', password='123')

    def test_other_event_view_status_code(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/muutapahtuma'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_form(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/muutapahtuma'
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, OtherEventForm)

    def test_csrf(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/muutapahtuma'
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_other_event_form_send(self):
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/muutapahtuma'
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

    def test_other_event_form_invalid_form_data(self):
        #Invalid post data should not redirect
        #The expected behavior is to show the form again with validation errors
        url = reverse('home',urlconf='riskiwww.urls')+'eventsignup/event/add/muutapahtuma'
        #urli=resolve('formtype')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
