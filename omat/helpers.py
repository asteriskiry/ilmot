# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, SitzForm
import random
from django.core.mail import send_mail

# Generoi uuden uniikin uid:n tapahtumalle.
def getUid():
	uid=random.randint(10000, 99999)
	events=Events.objects.all().values('uid')
	for field in events:
		if(field['uid']==uid):
			uid=random.randint(10000, 99999)
	return uid

# Palauttaa oikean tyyppisen form-olion, jotta saadaan oikeanlainen
# tapahtuma tallennettua.
def getForm(event_type,request):
	form=None
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

def getSignuForm(event_type,request):
	pass

# Palauttaa tietokannasta oikeanlaisen tapahtuman
# esikatselua varten.
def getEvent(uid):
	event=None
	tempevent=Events.objects.get(uid=uid)
#	events=Events.objects.all()
#	for field in events:
#		try:
#			if(field.uid==uid):
#				tempevent=Events.objects.get(uid=uid)
#		except ObjectDoesNotExist:
#			pass
	if(tempevent.event_type.event_type=='sitz'):
		event=Sitz.objects.get(uid=uid)
	elif(tempevent.event_type.event_type=='vuosijuhlat'):
		event=Annualfest.objects.get(uid=uid)
	elif(tempevent.event_type.event_type=='ekskursio'):
		event=Excursion.objects.get(uid=uid)
	elif(tempevent.event_type.event_type=='muu'):
		event=OtherEvent.objects.get(uid=uid)
	return event

# Generoi sähköpostin viestiosan.
def genMsg(data):
	prize=""
	if "€" in data.prize:
		prize=str(data.prize)
	else:
		prize=str(data.prize)+" €"
	return data.name+"\n\n"+str(data.owner)+"\n\n"+data.description+"\n\nIlmoittaudu tästä: http://212.32.242.196:7777/eventsignup/event/"+str(data.uid.uid)+"/signup\n\nMikä-Missä-Milloin:\n\nMikä: "+data.name+"\nMissä: "+data.place+"\nMilloin: "+str(data.date)+" klo: "+str(data.start_time)+"\nMitä maksaa: "+prize+"\n"

# Lähettää tapahtuman tiedot
# käyttäjälle rekisteröityyn sähköpostiosoitteeseen.
def sendEmail(data,request):
	send_mail(
    '[* tapahtumailmoittautumisjärjestelmä] Lisätty tapahtuma: '+data.name,
    genMsg(data),
    'noreply@asteriski.fi',
    ['foobar@example.com'],
    fail_silently=False,
	)

