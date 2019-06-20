# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent, Participant
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
import random
import json
from django.core import mail
from fpdf import FPDF, HTMLMixin


# Generoi uuden uniikin uid:n tapahtumalle.
def getUid():
    uid = random.randint(10000, 99999)
    events = list(Events.objects.values_list('uid', flat=True))
    while(events.count(uid) > 0):
        uid = random.randint(10000, 99999)
    return uid


# Palauttaa oikean tyyppisen form-olion, jotta saadaan oikeanlainen
# tapahtuma tallennettua.
def getForm(event_type, request, **kwargs):
    form = None
    initial = None
    if(kwargs and 'initial' in kwargs):
        initial = kwargs['initial']
    if(event_type == 'sitsit'):
        form = SitzForm(request.POST or None, request.FILES or None, instance=initial)
    elif(event_type == 'vuosijuhlat'):
        form = AnnualfestForm(request.POST or None, request.FILES or None, instance=initial)
    elif(event_type == 'ekskursio'):
        form = ExcursionForm(request.POST or None, request.FILES or None, instance=initial)
    elif(event_type == 'muutapahtuma'):
        form = OtherEventForm(request.POST or None, request.FILES or None, instance=initial)
    return form


# Palauttaa oikean tyyppisen form-olion editointia varten.
def getEditableForm(event):
    form = None
    if(event.event_type.event_type == 'sitsit'):
        form = SitzForm(initial={'name': event.name, 'place': event.place, 'date': event.date, 'start_time': event.start_time, 'description': event.description, 'prize': event.prize, 'max_participants': event.max_participants, 'signup_starts_date': event.signup_starts.date(), 'signup_starts_time': event.signup_starts.strftime("%X"), 'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"), 'quotas': event.quotas, 'has_reserve_spots': event.has_reserve_spots})
    elif(event.event_type.event_type == 'vuosijuhlat'):
        form = AnnualfestForm(initial={'name': event.name, 'place': event.place, 'date': event.date, 'start_time': event.start_time, 'description': event.description, 'prize': event.prize, 'max_participants': event.max_participants, 'signup_starts_date': event.signup_starts.date(), 'signup_starts_time': event.signup_starts.strftime("%X"), 'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"), 'has_reserve_spots': event.has_reserve_spots})
    elif(event.event_type.event_type == 'ekskursio'):
        form = ExcursionForm(initial={'name': event.name, 'place': event.place, 'date': event.date, 'end_date': event.end_date, 'start_time': event.start_time, 'description': event.description, 'pic': event.pic, 'prize': event.prize, 'max_participants': event.max_participants, 'signup_starts_date': event.signup_starts.date(), 'signup_starts_time': event.signup_starts.strftime("%X"), 'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"), 'has_reserve_spots': event.has_reserve_spots})
    elif(event.event_type.event_type == 'muutapahtuma'):
        form = OtherEventForm(initial={'name': event.name, 'place': event.place, 'date': event.date, 'start_time': event.start_time, 'description': event.description, 'prize': event.prize, 'max_participants': event.max_participants, 'signup_starts_date': event.signup_starts.date(), 'signup_starts_time': event.signup_starts.strftime("%X"), 'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"),'min_participants': event.min_participants, 'has_reserve_spots': event.has_reserve_spots})
    return form


# Palauttaa oikeanlaisen form-olion, jotta saadaan
# oikeanlainen tapahtumaanilmoittautuminen.
def getSignupForm(event_type, request):
    form = None
    if(event_type == 'sitsit'):
        form = SitzSignupForm(request.POST)
    elif(event_type == 'vuosijuhlat'):
        form = AnnualfestSignupForm(request.POST)
    elif(event_type == 'ekskursio'):
        form = ExcursionSignupForm(request.POST)
    elif(event_type == 'muutapahtuma'):
        form = OtherEventSignupForm(request.POST)
    elif(event_type == 'custom'):
        form = CustomSignupForm(request.POST)
    return form


# Palauttaa tietokannasta oikeanlaisen tapahtuman
# esikatselua varten.
def getEvent(uid):
    event = None
    tempevent = Events.objects.get(uid=uid)
    if(tempevent.event_type.event_type == 'sitsit'):
        event = Sitz.objects.get(uid=uid)
    elif(tempevent.event_type.event_type == 'vuosijuhlat'):
        event = Annualfest.objects.get(uid=uid)
    elif(tempevent.event_type.event_type == 'ekskursio'):
        event = Excursion.objects.get(uid=uid)
    elif(tempevent.event_type.event_type == 'muutapahtuma'):
        event = OtherEvent.objects.get(uid=uid)
    return event


# Generoi sähköpostin viestiosan.
def genMsg(data, request):
    prize = ""
    try:
        if "€" in data.prize:
            prize = str(data.prize)
        else:
            prize = str(data.prize)+" €"
    except:
        prize = "ilmainen"
    return data.name+"\n\n"+str(data.owner)+"\n\n"+data.description+"\n\nIlmoittaudu tästä: "+getBaseurl(request)+"/event/"+str(data.uid.uid)+"/signup\n\nTL;DR:\n\nMikä: "+data.name+"\nMissä: "+data.place+"\nMilloin: "+str(data.date)+" klo: "+str(data.start_time)+"\nMitä maksaa: "+prize+"\n"


# Lähettää tapahtuman tiedot
# käyttäjälle rekisteröityyn sähköpostiosoitteeseen.
def sendEmail(data, request):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            ' [* tapahtumailmoittautumisjärjestelmä] Lisätty tapahtuma: '+data.name, genMsg(data,request), 'noreply@asteriski.fi', [str(data.owner.email)],
            connection=connection,
            ).send()
#    send_mail(
#   '[* tapahtumailmoittautumisjärjestelmä] Lisätty tapahtuma: '+data.name,
#    genMsg(data,request),
#    'noreply@asteriski.fi',
#    [request.user.email],
#    fail_silently=False,
#    )


# Palauttaa listan, jossa on järjestävien tahojen nimet, mikäli on osallistujakiintiöitä.
def getQuotaNames(quotas, namesOnly):
    temp = quotas.split(",")
    paluu = []
    temp2 = []
    if(':' in temp[0]):
        for x in temp:
            temp2.append(x.split(":"))
    else:
        temp3 = []
        for x in temp:
            temp3.append(x.split())
        for x in temp3:
            temp4 = ''
            for y in x:
                if not str.isdigit(y):
                    temp4 += y
                temp2.append([temp4, temp3[-1]])

    if(namesOnly):
        for y in temp2:
            paluu.append(y[0])
    else:
        return temp2
    return paluu


# Generoi tapahtumaan ilmoittautujaan tallennettavia lisätietoja.
def getMiscInfo(data):
    return json.dumps({'member': False, 'hasPaid': False})


def getBaseurl(request):
    protocol = 'http'
    if(request.is_secure()):
        protocol = 'https'
    return protocol+'://'+request.META['HTTP_HOST']


# Palauttaa dictionaryn, jossa on {uid:osallistujamäärä}
def getParticipantCount():
    events = Events.objects.all()
    numOfParticipants = {}
    for event in events:
        uid = str(event.uid)
        numOfParticipants[uid] = Participant.objects.filter(event_type_id=event.uid).count()
        # numOfParticipants.update(uid=Participant.objects.filter(event_type_id=event.uid).count())
    return numOfParticipants


def isQuotaFull(event,data):
    try:
        #	haettu quota on data['name']
        quotas=getQuotaNames(event.quotas,False)
        numOf=Participant.objects.filter(event_type=event.uid).filter(miscInfo__contains=data['name']).count()
        paluu=False
    except AttributeError as e:
        paluu=False
    return paluu

class HTML2PDF(FPDF, HTMLMixin):
    pass
# Generoi tapahtuman osallistujalistan pdf muotoon.
def genPdf(request,participants,event):
    from django.template import loader
    from django.conf import settings
    nimi='osallistujalista_'+str(event.name).replace(' ','_')+'.pdf'
    template = loader.get_template("eventsignup/includes/participant_table.html")
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(template.render({'event': event, 'participants': participants}, request))
    pdf.output(settings.MEDIA_ROOT+'/'+nimi)
    return nimi
