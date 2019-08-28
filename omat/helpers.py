# Erilaiset omat apufunktiot tänne.
# Käyttö: from omat import helpers ja helpers.<funktion_nimi>
import csv
import random
from datetime import datetime
from zipfile import ZipFile

from django.core import mail
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table

from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, \
    CustomSignupForm
from eventsignup.models import Events, Sitz, Annualfest, Excursion, OtherEvent, Participant


# from reportlab.lib.pagesizes import landscape, A4
# from reportlab.lib.units import cm


# Generoi uuden uniikin uid:n tapahtumalle.
def get_uid():
    uid = random.randint(10000, 99999)
    events = list(Events.objects.values_list('uid', flat=True))
    while events.count(uid) > 0:
        uid = random.randint(10000, 99999)
    return uid


# Palauttaa oikean tyyppisen form-olion, jotta saadaan oikeanlainen
# tapahtuma tallennettua.
def get_form(event_type, request, **kwargs):
    form = None
    initial = None
    if kwargs and 'initial' in kwargs:
        initial = kwargs['initial']
    if event_type == 'sitsit':
        form = SitzForm(request.POST or None, request.FILES or None, instance=initial)
    elif event_type == 'vuosijuhlat':
        form = AnnualfestForm(request.POST or None, request.FILES or None, instance=initial)
    elif event_type == 'ekskursio':
        form = ExcursionForm(request.POST or None, request.FILES or None, instance=initial)
    elif event_type == 'muutapahtuma':
        form = OtherEventForm(request.POST or None, request.FILES or None, instance=initial)
    return form


# Palauttaa oikean tyyppisen form-olion editointia varten.
def get_editable_form(event):
    form = None
    if event.event_type.event_type == 'sitsit':
        form = SitzForm(
            initial={'name': event.name, 'place': event.place, 'date': event.date, 'start_time': event.start_time,
                     'description': event.description, 'prize': event.prize, 'max_participants': event.max_participants,
                     'signup_starts_date': event.signup_starts.date(),
                     'signup_starts_time': event.signup_starts.strftime("%X"),
                     'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"),
                     'quotas': event.quotas, 'has_reserve_spots': event.has_reserve_spots})
    elif event.event_type.event_type == 'vuosijuhlat':
        form = AnnualfestForm(
            initial={'name': event.name, 'place': event.place, 'date': event.date, 'start_time': event.start_time,
                     'description': event.description, 'prize': event.prize, 'max_participants': event.max_participants,
                     'signup_starts_date': event.signup_starts.date(),
                     'signup_starts_time': event.signup_starts.strftime("%X"),
                     'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"),
                     'has_reserve_spots': event.has_reserve_spots})
    elif event.event_type.event_type == 'ekskursio':
        form = ExcursionForm(
            initial={'name': event.name, 'place': event.place, 'date': event.date, 'end_date': event.end_date,
                     'start_time': event.start_time, 'description': event.description, 'pic': event.pic,
                     'prize': event.prize, 'max_participants': event.max_participants,
                     'signup_starts_date': event.signup_starts.date(),
                     'signup_starts_time': event.signup_starts.strftime("%X"),
                     'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"),
                     'has_reserve_spots': event.has_reserve_spots})
    elif event.event_type.event_type == 'muutapahtuma':
        form = OtherEventForm(
            initial={'name': event.name, 'place': event.place, 'date': event.date, 'start_time': event.start_time,
                     'description': event.description, 'prize': event.prize, 'max_participants': event.max_participants,
                     'signup_starts_date': event.signup_starts.date(),
                     'signup_starts_time': event.signup_starts.strftime("%X"),
                     'signup_ends_date': event.signup_ends.date(), 'signup_ends_time': event.signup_ends.strftime("%X"),
                     'min_participants': event.min_participants, 'has_reserve_spots': event.has_reserve_spots})
    return form


# Palauttaa oikeanlaisen form-olion, jotta saadaan
# oikeanlainen tapahtumaanilmoittautuminen.
def get_signup_form(event_type, request):
    form = None
    if event_type == 'sitsit':
        form = SitzSignupForm(request.POST)
    elif event_type == 'vuosijuhlat':
        form = AnnualfestSignupForm(request.POST)
    elif event_type == 'ekskursio':
        form = ExcursionSignupForm(request.POST)
    elif event_type == 'muutapahtuma':
        form = OtherEventSignupForm(request.POST)
    elif event_type == 'custom':
        form = CustomSignupForm(request.POST)
    return form


# Palauttaa tietokannasta oikeanlaisen tapahtuman
# esikatselua varten.
def get_event(uid):
    event = None
    tempevent = Events.objects.get(uid=uid)
    if tempevent.event_type.event_type == 'sitsit':
        event = Sitz.objects.get(uid=uid)
    elif tempevent.event_type.event_type == 'vuosijuhlat':
        event = Annualfest.objects.get(uid=uid)
    elif tempevent.event_type.event_type == 'ekskursio':
        event = Excursion.objects.get(uid=uid)
    elif tempevent.event_type.event_type == 'muutapahtuma':
        event = OtherEvent.objects.get(uid=uid)
    return event


# Generoi sähköpostin viestiosan.
def gen_msg(data, request):
    prize = ""
    try:
        if "€" in data.prize:
            prize = str(data.prize)
        else:
            prize = str(data.prize) + " €"
    except:
        prize = "ilmainen"
    return data.name + "\n\n" + str(data.owner) + "\n\n" + data.description + "\n\nIlmoittaudu tästä: " + get_baseurl(
        request) + "/event/" + str(
        data.uid.uid) + "/signup\n\nTL;DR:\n\nMikä: " + data.name + "\nMissä: " + data.place + "\nMilloin: " + str(
        data.date) + " klo: " + str(data.start_time) + "\nMitä maksaa: " + prize + "\n"


# Lähettää tapahtuman tiedot
# käyttäjälle rekisteröityyn sähköpostiosoitteeseen.
def send_email(data, request):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            ' [* tapahtumailmoittautumisjärjestelmä] Lisätty tapahtuma: ' + data.name, gen_msg(data, request),
            'noreply@asteriski.fi', [str(data.owner.email)],
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
def get_quota_names(quotas, names_only):
    temp = quotas.split(",")
    paluu = []
    temp2 = []
    if ':' in temp[0]:
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

    if names_only:
        for y in temp2:
            paluu.append(y[0])
    else:
        return temp2
    return paluu


def get_baseurl(request):
    protocol = 'http'
    if request.is_secure():
        protocol = 'https'
    return protocol + '://' + request.META['HTTP_HOST']


# Palauttaa dictionaryn, jossa on {uid:osallistujamäärä}
def get_participant_count():
    events = Events.objects.all()
    num_of_participants = {}
    for event in events:
        uid = str(event.uid)
        num_of_participants[uid] = Participant.objects.filter(event_type_id=event.uid).count()
        # numOfParticipants.update(uid=Participant.objects.filter(event_type_id=event.uid).count())
    return num_of_participants


def is_quota_full(event, data):
    try:
        #	haettu quota on data['name']
        quotas = get_quota_names(event.quotas, False)
        num_of = Participant.objects.filter(event_type=event.uid).filter(miscInfo__contains=data['name']).count()
        paluu = False
    except AttributeError as e:
        paluu = False
    return paluu


# Generoi taulukon osallistujista ja tekee siitä pdf tiedoston
# Palauttaa luodun tiedoston nimen
def gen_pdf(event, participants, directory):
    file_name = 'osallistujalista_' + str(event.name).replace(' ',
                                                              '_') + '_' + datetime.today().date().isoformat() + '.pdf'
    model_keys = Participant._meta.__dict__.get("fields")
    model_keys = [f.name for f in model_keys if not (f.name == 'id' or f.name == 'event_type')]
    data = [model_keys]
    for participant in participants:
        del participant['id']
        del participant['event_type_id']
        data.append(participant.values())
    table = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black)])
    styles = getSampleStyleSheet()
    title = Paragraph("Osallistujalista %s" % str(event.name), styles["Heading1"])
    doc = SimpleDocTemplate(directory + '/' + file_name)
    # elements = [Spacer(1, 2 * cm)]
    elements = []
    elements.append(title)
    elements.append(table)
    # elements.append(Spacer(1, 0.2 * cm))
    doc.build(elements)
    return file_name


# Generoi excel-tyylisen pilkulla erotetun csv tiedoston kaikista tapahtuman osallistujista
# Palauttaa generoidun tiedoston nimen
def gen_csv(event, participants, directory):
    file_name = 'osallistujalista_' + str(event.name).replace(' ',
                                                              '_') + '_' + datetime.today().date().isoformat() + '.csv'
    model_keys = Participant._meta.__dict__.get("fields")
    model_keys = [f.name for f in model_keys if not (f.name == 'id' or f.name == 'event_type')]
    with open(directory + '/' + file_name, 'w') as csvfile:
        fieldnames = list(model_keys)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel', delimiter=',')
        writer.writeheader()
        for participant in participants:
            participant_row = {}
            for key in model_keys:
                participant_row[key] = participant[key]
            writer.writerow(participant_row)
    return file_name


# Generoi kaikki valitut export formaatit sisältävän zip-tiedoston
# Palauttaa luodun tiedoston nimen
def gen_zip(event, participants, list_of_exports, directory):
    file_name = 'osallistujalista_' + str(event.name).replace(' ',
                                                              '_') + '_' + datetime.today().date().isoformat() + '.zip'
    file_names = []
    if 'csv' in list_of_exports:
        file_names.append(gen_csv(event, participants, directory))
    if 'pdf' in list_of_exports:
        file_names.append(gen_pdf(event, participants, directory))
    # for file in file_names:
    #     shutil.move(directory+file, directory)
    # shutil.make_archive(file_name, 'zip', base_dir='.', root_dir=directory)
    with ZipFile(directory + '/' + file_name, 'w') as myzip:
        for file in file_names:
            myzip.write(directory + '/' + file, arcname='./' + file)
    # file_name = file_name+'.zip'
    # shutil.move(file_name, path)
    return file_name


# Entry point metodi erityyppisille tiedostoexporteille
# Palauttaa exportattavan tiedoston nimen
def gen_export(event, type_of_export, participants, list_of_exports, directory, **kwargs):
    if type_of_export == 'csv':
        return gen_csv(event, participants, directory)
    elif type_of_export == 'pdf':
        return gen_pdf(event, participants, directory)
    elif type_of_export == 'zip':
        return gen_zip(event, participants, list_of_exports, directory)


def get_export_options():
    return ['csv', 'pdf']
