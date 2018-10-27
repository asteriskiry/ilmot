# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent, Participant
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
import random, json
from django.core import mail

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
		form=SitzForm(request.POST,request.FILES)
	elif(event_type=='vuosijuhlat'):
		form=AnnualfestForm(request.POST,request.FILES)
	elif(event_type=='ekskursio'):
		form=ExcursionForm(request.POST,request.FILES)
	elif(event_type=='muutapahtuma'):
		form=OtherEventForm(request.POST,request.FILES)
	return form

# Palauttaa oikeanlaisen form-olion, jotta saadaan
# oikeanlainen tapahtumaanilmoittautuminen.
def getSignupForm(event_type,request):
	form=None
	if(event_type=='sitsit'):
		form=SitzSignupForm(request.POST)
	elif(event_type=='vuosijuhlat'):
		form=AnnualfestSignupForm(request.POST)
	elif(event_type=='ekskursio'):
		form=ExcursionSignupForm(request.POST)
	elif(event_type=='muu'):
		form=OtherEventSignupForm(request.POST)
	elif(event_type=='custom'):
		form=CustomSignupForm(request.POST)
	return form

# Palauttaa tietokannasta oikeanlaisen tapahtuman
# esikatselua varten.
def getEvent(uid):
	event=None
	tempevent=Events.objects.get(uid=uid)
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
def genMsg(data,request):
	prize=""
	try:
		if "€" in data.prize:
			prize=str(data.prize)
		else:
			prize=str(data.prize)+" €"
	except:
		prize="ilmainen"
	return data.name+"\n\n"+str(data.owner)+"\n\n"+data.description+"\n\nIlmoittaudu tästä: "+getBaseurl(request)+"/eventsignup/event/"+str(data.uid.uid)+"/signup\n\nMikä-Missä-Milloin:\n\nMikä: "+data.name+"\nMissä: "+data.place+"\nMilloin: "+str(data.date)+" klo: "+str(data.start_time)+"\nMitä maksaa: "+prize+"\n"

# Lähettää tapahtuman tiedot
# käyttäjälle rekisteröityyn sähköpostiosoitteeseen.
def sendEmail(data,request):
	with mail.get_connection() as connection:
	    mail.EmailMessage(
       ' [* tapahtumailmoittautumisjärjestelmä] Lisätty tapahtuma: '+data.name, genMsg(data,request), 'noreply@asteriski.fi', [str(data.owner.email)],
        connection=connection,
   		 ).send()
#	send_mail(
#   '[* tapahtumailmoittautumisjärjestelmä] Lisätty tapahtuma: '+data.name,
#    genMsg(data,request),
#    'noreply@asteriski.fi',
#    [request.user.email],
#    fail_silently=False,
#	)

# Palauttaa listan, jossa on järjestävien tahojen nimet, mikäli on osallistujakiintiöitä.
def getQuotaNames(quotas,namesOnly):
	temp=quotas.split(",")
	paluu=[]
	temp2=[]
	if(':' in temp[0]):
		for x in temp:
			temp2.append(x.split(":"))
	else:
		temp3=[]
		for x in temp:
			temp3.append(x.split())
		for x in temp3:
			temp4=''
			for y in x:
				if not str.isdigit(y):
					temp4+=y
				temp2.append([temp4,temp3[-1]])

	if(namesOnly):
		for y in temp2:
			paluu.append(y[0])
	else:
		return temp2
	return paluu

# Generoi tapahtumaan ilmoittautujaan tallennettavia lisätietoja.
def getMiscInfo(data):
	lihaton=False
	holiton=True
	if(data['lihaton']=='kasvis'):
		lihaton=True
	if(data['holiton']=='holillinen'):
		holiton=False
	return json.dumps({'lihaton': lihaton, 'holiton':holiton, 'member':False, 'hasPaid':False, 'avec':data['avec'], 'plaseeraus':data['plaseeraus'],'quota':data['name']})

def getBaseurl(request):
	protocol='http'
	if(request.is_secure()):
		protocol='https'
	return protocol+'://'+request.META['HTTP_HOST']+'/eventsignup'

# Palauttaa dictionaryn, jossa on {uid:osallistujamäärä}
def getParticipantCount():
	events=Events.objects.all()
	numOfParticipants={}
	for event in events:
		uid=str(event.uid)
		numOfParticipants[uid]=Participant.objects.filter(event_type_id=event.uid).count()
		#numOfParticipants.update(uid=Participant.objects.filter(event_type_id=event.uid).count())
	return numOfParticipants

# Palauttaa True/False riippuen siitä onko ilmoittautumiskiintiö täynnä.
def isQuotaFull(event,data):
#	haettu quota on data['name']
	quotas=getQuotaNames(event.quotas,False)
	numOf=Participant.objects.filter(event_type=event.uid).filter(miscInfo__contains=data['name']).count()
	paluu=False
#	json.loads(
	return paluu

