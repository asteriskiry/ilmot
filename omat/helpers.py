# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent
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
#	form=None
	if(event_type=='Sitsit'):
#		form=SitzForm(request.POST)
		return SitzForm(request.POST)
	elif(event_type=='Vuosijuhlat'):
#		form=AnnualfestForm(request.POST)
		return AnnualfestForm(request.POST)
	elif(event_type=='Ekskursio'):
#		form=ExcursionForm(request.POST)
		return ExcursionForm(request.POST)
	elif(event_type=='Muu'):
#		form=OtherEventForm(request.POST)
		return OtherEventForm(request.POST)
#	return form

def getEvent(uid):
	event=None
	tempevent=None
	events=Events.all()
	for field in events:
		try:
			if(field['uid']==uid):
				tempevent=Events.objects.get(uid=uid)
		except ObjectDoesNotExist:
			pass
	if(tempevent['event_type']=='Sitsit'):
		return Sitz.objects.get(uid=uid)
	elif(tempevent['event_type']=='Vuosijuhlat'):
		return Annualfest.objects.get(uid=uid)
	elif(tempevent['event_type']=='Ekskursio'):
		return Excursion.objects.get(uid=uid)
	elif(tempevent['event_type']=='Muu'):
		return OtherEvent.objects.get(uid=uid)
