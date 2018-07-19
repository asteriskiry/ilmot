# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, SitzForm
import random
from django.core.exceptions import ObjectDoesNotExist

def getUid():
	uid=random.randint(10000, 99999)
	events=Events.objects.all().values('uid')
	for field in events:
		if(field['uid']==uid):
			uid=random.randint(10000, 99999)
	return uid

def getForm(event_type,request):
	form=None
	print(event_type)
	if(event_type=='sitsit'):
		form=SitzForm(request.POST)
#		return SitzForm(request.POST)
	elif(event_type=='vuosijuhlat'):
		form=AnnualfestForm(request.POST)
#		return AnnualfestForm(request.POST)
	elif(event_type=='ekskursio'):
		form=ExcursionForm(request.POST)
#		return ExcursionForm(request.POST)
	elif(event_type=='muu'):
		form=OtherEventForm(request.POST)
#		return OtherEventForm(request.POST)
	return form

def getEvent(uid):
#	event=None
	tempevent=Events.objects.get(uid=uid)
#	events=Events.objects.all()
#	for field in events:
#		try:
#			if(field['uid']==uid):
#				tempevent=Events.objects.get(uid=uid)
#		except ObjectDoesNotExist:
#			pass
	if(tempevent['event_type']=='sitsit'):
		return Sitz.objects.get(uid=uid)
	elif(tempevent['event_type']=='vuosijuhlat'):
		return Annualfest.objects.get(uid=uid)
	elif(tempevent['event_type']=='ekskursio'):
		return Excursion.objects.get(uid=uid)
	elif(tempevent['event_type']=='muu'):
		return OtherEvent.objects.get(uid=uid)
