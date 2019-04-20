from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.http import HttpResponseRedirect
from .models import EventType, Events, Sitz, Annualfest, Excursion, OtherEvent, Participant, Archive
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
from omat import helpers
from datetime import datetime, timezone


# Koko järjestelmän juuri (= /) sivu.
def index(request):
    return render(request, "eventsignup/index.html", {'baseurl': helpers.getBaseurl(request)})


# Tapahtumaan ilmoittautumisen jälkeen näytettävä kiitossivu.
def thanks(request, **kwargs):
    # refereristä uid, jotta event.name ja owner.email saadaan tietokannasta.
    event = None
    temp = None
    if(kwargs):
        if(kwargs['type'] == '2'):
            reserve = True
        else:
            reserve = False
    try:
        temp = request.META['HTTP_REFERER'].split("/")
        for x in temp:
            if(str.isdigit(x)):
                uid = int(x)
#        uid=''.join(filter(str.isdigit, request.META['HTTP_REFERER']))
        event = helpers.getEvent(uid)
    except KeyError:
        return HttpResponseRedirect('/')
    except OverflowError:
        pass
    return render(request, "eventsignup/thankyou.html", {'event': event, 'baseurl': helpers.getBaseurl(request), 'page': 'Ilmoittaudu', 'reserve': reserve})


# Jos on max määrä osallistujia jo, näytetään tämä.
def failed(request):
    return render(request, "eventsignup/failed.html", {'baseurl': helpers.getBaseurl(request)})


# GDPR/tietosuojatiedot
def privacy(request):
    return render(request, "eventsignup/privacy.html", {'baseurl': helpers.getBaseurl(request)})


# Tuottaa ja palauttaa oikeaann sivupaneeliin tulevat widgetin nippelitiedot.
@login_required
def stats(request, uid):
    pass


# Tuottaa ilmoittautumislomakkeen uid:tä vastaavaan tapahtumaan.
# Käsittelee ja tallentaa lomakkeelta tulevan ilmoittautumisen.
def signup(request, uid):
    temp = Events.objects.get(uid=uid)
    event_type = temp.event_type.event_type
    event = helpers.getEvent(uid)
    maxParticipants = Participant.objects.filter(event_type=uid, reserve_spot=False).count() == event.max_participants
    if(not event.has_reserve_spots and maxParticipants):
        return HttpResponseRedirect('/failed')
    if(request.method == 'POST'):
        form = helpers.getSignupForm(event_type, request)
        if(form.is_valid()):
            # käsittele lomake
            if(helpers.isQuotaFull(event, form.cleaned_data)):
                return HttpResponseRedirect('/failed')
            data = form.save(commit=False)
            lihaton = False
            holiton = True
            try:
                if(form.cleaned_data['lihaton'] == 'kasvis'):
                    lihaton = True
                elif(form.cleaned_data['lihaton'] == 'null'):
                    lihaton = None
                if(form.cleaned_data['holiton'] == 'holillinen'):
                    holiton = False
                elif(form.cleaned_data['holiton'] == 'null'):
                    holiton = None
                if(form.cleaned_data['gender'] == 'null'):
                    data.gender = None
                data.avec = form.cleaned_data['avec']
                data.plaseeraus = form.cleaned_data['plaseeraus']
            except KeyError:
                pass
            if(event.has_reserve_spots and maxParticipants):
                data.reserve_spot = True
                reserve = '2'
            else:
                data.reserve_spot = False
                reserve = '1'
            data.vege = lihaton
            data.nonholic = holiton
            data.avec = form.cleaned_data['avec']
            data.plaseeraus = form.cleaned_data['plaseeraus']
            if('organization' in request.POST):
                data.quota = request.POST['organization']
            else:
                data.quota = ''
            data.miscInfo = helpers.getMiscInfo(form.cleaned_data)
            data.event_type = temp
            data.save()
            return HttpResponseRedirect('/thanks/'+reserve)
    else:
        quotas = None
        canSignup = False
        signupPassed = False
        now = datetime.now(timezone.utc)
        participants = Participant.objects.filter(event_type=uid)
        if(event.signup_starts is not None and event.signup_starts <= now):
            canSignup = True
        if(event.signup_ends is not None and event.signup_ends <= now):
            signupPassed = True
        if(event_type == 'sitsit'):
            form = SitzSignupForm()
        elif(event_type == 'vuosijuhlat'):
            form = AnnualfestSignupForm()
        elif(event_type == 'ekskursio'):
            form = ExcursionSignupForm()
        elif(event_type == 'muutapahtuma'):
            form = OtherEventSignupForm()
        elif(event_type == 'custom'):
            form = CustomSignupForm()
    try:
        if(len(event.quotas) > 0):
            quotas = helpers.getQuotaNames(event.quotas, True)
    except AttributeError:
        pass
    return render(request, "eventsignup/signup.html", {'form': form, 'event': event, 'quotas': quotas, 'cansignup': canSignup, 'signuppassed': signupPassed, 'page': 'Ilmoittaudu', 'participants': participants, 'baseurl': helpers.getBaseurl(request)})


# Arkistoi tapahtuman erilliseen arkistoon (säilyttää vain olennaisimmat tapahtuman tiedot.
# Poistaa tämän jälkeen varsinaisen tapahtuman kannasta osallistujineen.
# Arkisto on vain ylläpitäjien nähtävissä.
@login_required
def archive(request, uid):
    event = helpers.getEvent(uid)
    archiveEvent = Archive(event_type=event.event_type, name=event.name, description=event.description, participants=Participant.objects.filter(event_type=uid).count(), owner=event.owner, date=event.date, place=event.place, pic=event.pic, prize=event.prize)
    archiveEvent.save()
    Events.objects.filter(uid=uid).delete()
    return render(request, "eventsignup/delete_success.html", {'baseurl': helpers.getBaseurl(request)})


# Tuottaa lomakeen uuden tapahtuman luomiseksi ja käsittelee sen.
@login_required
def add(request, **kwargs):
    desktop = True
    if('Mobi'in request.META['HTTP_USER_AGENT']):
        desktop = False
    if kwargs:
        event_type = kwargs['type']
    if(request.method == 'POST'):
        uid = helpers.getUid()
        form = helpers.getForm(event_type,request)
        if(form.is_valid()):
            User = get_user_model()
            event = Events(event_type, uid, request.user.get_username())
            event.save()
            data = form.save(commit=False)
            data.uid = Events.objects.get(uid=uid)
            data.event_type = EventType.objects.get(event_type=event_type)
#            data.owner=EventOwner.objects.get(name=request.user.get_username())
            data.owner = User.objects.get(username=request.user.get_username())
            #data.description = data.description.replace("\n", "</p><p>")
            data.signup_starts = datetime.combine(form.cleaned_data['signup_starts_date'], form.cleaned_data['signup_starts_time'], tzinfo=timezone.utc)
            data.signup_ends = datetime.combine(form.cleaned_data['signup_ends_date'], form.cleaned_data['signup_ends_time'], tzinfo=timezone.utc)
            data.save()
            helpers.sendEmail(data, request)
            return HttpResponseRedirect('/event/'+str(uid)+'/preview/')
    else:
        if(event_type == 'sitsit'):
            form = SitzForm()
        elif(event_type == 'vuosijuhlat'):
            form = AnnualfestForm()
        elif(event_type == 'ekskursio'):
            form = ExcursionForm()
        elif(event_type == 'muutapahtuma'):
            form = OtherEventForm()
        elif(event_type == 'custom'):
            form = CustomForm()
    return render(request, "eventsignup/new_event.html", {'form': form, 'edit': False, 'desktop': desktop, 'page': 'Lisää tapahtuma', 'baseurl': helpers.getBaseurl(request)})


# Lomake tapahtumatyypin valintaan ennen varsinaista lomaketta.
@login_required
def formtype(request, **kwargs):
    # sitsit, vujut, eksku, muu, custom
    if(request.method == 'POST'):
        temp = request.POST.get('choice')
        if(temp == 'sitsit'):
            return HttpResponseRedirect('/event/add/'+temp)
        elif(temp == 'vuosijuhlat'):
            return HttpResponseRedirect('/event/add/'+temp)
        elif(temp == 'ekskursio'):
            return HttpResponseRedirect('/event/add/'+temp)
        elif(temp == 'muutapahtuma'):
            return HttpResponseRedirect('/event/add/'+temp)
        elif(temp == 'custom'):
            return HttpResponseRedirect('/event/add/'+temp)
    else:
        form = SelectTypeForm()
    return render(request, "eventsignup/new_event.html", {'form': form, 'choice': True, 'page': 'Lisää tapahtuma', 'baseurl': helpers.getBaseurl(request)})


# Näyttää tapahtuman tiedot ja osallistujalistan.
@login_required
def info(request, uid,**kwargs):
	if(request.method=='POST'):
		Participant.objects.filter(event_type=uid,email=request.POST['user']).delete()
		return HttpResponseRedirect('/event/'+str(uid)+'/view/')
	else:
		just_list=False
		participants=Participant.objects.filter(event_type=uid)
		event=helpers.getEvent(uid)
		if(kwargs):
			if(kwargs['type']=='list'):
				just_list=True
			elif(kwargs['type']=='pdf'):
				pdf=helpers.genPdf(request,participants,event)
				return HttpResponseRedirect('/media/'+pdf)
		other=False
		return render(request,"eventsignup/view_event.html",{'other':other,'just_list':just_list,'event':event,'participants':participants,'page':'Tarkastele tapahtumaa','baseurl':helpers.getBaseurl(request)})


# Sisäänkirjautumisen jälkeen näytettävä "hallintapaneeli".
# Listaa sisäänkirjautuneen käyttäjän nykyiset ja menneet (ei arkistoidut) tapahtumat.
# Mahdollistaa myös niiden muokkauksen.
@login_required
def management(request):

    desktop = True
    if('Mobi'in request.META['HTTP_USER_AGENT']):
        desktop = False
    participantCount = helpers.getParticipantCount()
    auth_user = request.user.get_username()
    startdate = datetime.now()
    todaysdate = startdate.strftime("%Y-%m-%d")
    #
    #
    upcoming_sitz = Sitz.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_sitz = Sitz.objects.filter(date__lt=todaysdate, owner=auth_user)

    upcoming_otherEvents = OtherEvent.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_otherEvents = OtherEvent.objects.filter(date__lt=todaysdate, owner=auth_user)

    upcoming_excursion = Excursion.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_excursion = Excursion.objects.filter(date__lt=todaysdate, owner=auth_user)

    upcoming_annualfest = Annualfest.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_annualfest = Annualfest.objects.filter(date__lt=todaysdate, owner=auth_user)
    # eventit = list(chain(sitsit, ekskursiot, vujut, muut_tapahtumat))
    return render(request, "eventsignup/management.html",
    {'menneet_sitsit': previous_sitz, 'tulevat_sitsit': upcoming_sitz,
     'menneet_muutTapahtumat': previous_otherEvents, 'tulevat_muutTapahtumat': upcoming_otherEvents,
     'menneet_ekskursiot': previous_excursion, 'tulevat_ekskursiot': upcoming_excursion,
     'menneet_vujut': previous_annualfest, 'tulevat_vujut': upcoming_annualfest,
     'baseurl': helpers.getBaseurl(request), 'osallistujamaarat': helpers.getParticipantCount(), 'desktop': desktop, 'management': True,
    }
    )

# Olemassa olevan tapahtuman muokkaus.
@login_required
def edit(request, **kwargs):
    event = helpers.getEvent(kwargs['uid'])
    form = helpers.getEditableForm(event)
    desktop = True
    if(request.method == 'POST'):
        form = helpers.getForm(event.event_type.event_type, request, initial=event)
        if(form.is_valid()):
            data = form.save(commit=False)
            data.signup_starts = datetime.combine(form.cleaned_data['signup_starts_date'], form.cleaned_data['signup_starts_time'], tzinfo=timezone.utc)
            data.signup_ends = datetime.combine(form.cleaned_data['signup_ends_date'], form.cleaned_data['signup_ends_time'], tzinfo=timezone.utc)
            data.save()
            helpers.sendEmail(data, request)
            return HttpResponseRedirect('/event/'+str(event.uid.uid)+'/preview/edit')
    else:
        if('Mobi'in request.META['HTTP_USER_AGENT']):
            desktop = False
    return render(request, "eventsignup/new_event.html", {'event': event, 'form': form, 'edit': True,'page': 'Muokkaa tapahtumaa', 'desktop': desktop, 'baseurl': helpers.getBaseurl(request)})


# Uuden tapahtuman luonnin jälkeen näytettävä esikatselu.
@login_required
def preview(request, uid, **kwargs):
#    url = reverse('home',urlconf='riskiwww.urls')+"eventsignup"
    event = helpers.getEvent(uid)
    edit = False
    if(kwargs and kwargs['type'] == 'edit'):
        edit = True
    return render(request, "eventsignup/preview.html", {'event': event, 'edit': edit, 'baseurl': helpers.getBaseurl(request)})
