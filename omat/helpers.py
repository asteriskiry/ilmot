# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
import random, json
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
	elif(event_type=='muutapahtuma'):
		form=OtherEventForm(request.POST)
#		return OtherEventForm(request.POST)
	return form

def getSignupForm(event_type,request):
	form=None
	if(event_type=='sitsit'):
		form=SitzSignupForm(request.POST)
#		return SitzForm(request.POST)
	elif(event_type=='vuosijuhlat'):
		form=AnnualfestSignupForm(request.POST)
#		return AnnualfestForm(request.POST)
	elif(event_type=='ekskursio'):
		form=ExcursionSignupForm(request.POST)
#		return ExcursionForm(request.POST)
	elif(event_type=='muu'):
		form=OtherEventSignupForm(request.POST)
#		return OtherEventForm(request.POST)
	elif(event_type=='custom'):
		form=CustomSignupForm(request.POST)
	return form

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
	if(tempevent.event_type.event_type=='sitsit'):
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
	try:
		if "€" in data.prize:
			prize=str(data.prize)
		else:
			prize=str(data.prize)+" €"
	except:
		prize="ilmainen"
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

def getQuotaNames(quotas):
	temp=quotas.split(",")
	paluu=[]
	temp2=[]
	for x in temp:
		temp2.append(x.split(":"))
	for y in temp2:
		paluu.append(y[0])
	return paluu

def getMiscInfo(data):
	lihaton=False
	holiton=True
	if(data['lihaton']=='kasvis'):
		lihaton=True
	if(data['holiton']=='holillinen'):
		holiton=False
	return json.dumps({'lihaton': lihaton, 'holiton':holiton, 'member':False, 'hasPaid':False, 'avec':data['avec'], 'plaseeraus':data['plaseeraus']})

