from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import EventType, Events, Sitz, Annualfest, Excursion, OtherEvent, Participant, Archive
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, \
    CustomSignupForm

from omat import helpers
from omat.seating_arrangement import make_seating
from datetime import datetime, timezone
import mimetypes
import tempfile
from pathlib import Path


# Koko järjestelmän juuri (= /) sivu.
def index(request):
    return render(request, "eventsignup/index.html", {'baseurl': helpers.get_baseurl(request)})


# Tapahtumaan ilmoittautumisen jälkeen näytettävä kiitossivu.
def thanks(request, **kwargs):
    # refereristä uid, jotta event.name ja owner.email saadaan tietokannasta.
    event = None
    temp = None
    if kwargs:
        if kwargs['type'] == '2':
            reserve = True
        else:
            reserve = False
    try:
        temp = request.META['HTTP_REFERER'].split("/")
        for x in temp:
            if str.isdigit(x):
                uid = int(x)
        #        uid=''.join(filter(str.isdigit, request.META['HTTP_REFERER']))
        event = helpers.get_event(uid)
    except KeyError:
        return HttpResponseRedirect('/')
    except OverflowError:
        pass
    return render(request, "eventsignup/thankyou.html",
                  {'event': event, 'baseurl': helpers.get_baseurl(request), 'page': 'Ilmoittaudu', 'reserve': reserve})


# Jos on max määrä osallistujia jo, näytetään tämä.
def failed(request):
    return render(request, "eventsignup/failed.html", {'baseurl': helpers.get_baseurl(request)})


# GDPR/tietosuojatiedot
def privacy(request):
    return render(request, "eventsignup/privacy.html", {'baseurl': helpers.get_baseurl(request)})


# Tuottaa ja palauttaa oikeaann sivupaneeliin tulevat widgetin nippelitiedot.
@login_required
def stats(request, uid):
    pass


# Tuottaa ilmoittautumislomakkeen uid:tä vastaavaan tapahtumaan.
# Käsittelee ja tallentaa lomakkeelta tulevan ilmoittautumisen.
def signup(request, uid):
    temp = Events.objects.get(uid=uid)
    event_type = temp.event_type.event_type
    event = helpers.get_event(uid)
    max_participants = Participant.objects.filter(event_type=uid, reserve_spot=False).count() == event.max_participants
    if not event.has_reserve_spots and max_participants:
        return HttpResponseRedirect('/failed')
    if request.method == 'POST':
        form = helpers.get_signup_form(event_type, request)
        if form.is_valid():
            if helpers.is_quota_full(event, form.cleaned_data):
                return HttpResponseRedirect('/failed')
            data = form.save(commit=False)
            lihaton = False
            holiton = True
            try:
                if form.cleaned_data['lihaton'] == 'kasvis':
                    lihaton = True
                elif form.cleaned_data['lihaton'] == 'null':
                    lihaton = None
                if form.cleaned_data['holiton'] == 'holillinen':
                    holiton = False
                elif form.cleaned_data['holiton'] == 'null':
                    holiton = None
                if form.cleaned_data['gender'] == 'null':
                    data.gender = None
                data.avec = form.cleaned_data['avec']
                data.plaseeraus = form.cleaned_data['plaseeraus']
            except KeyError:
                pass
            if event.has_reserve_spots and max_participants:
                data.reserve_spot = True
                reserve = '2'
            else:
                data.reserve_spot = False
                reserve = '1'
            data.vege = lihaton
            data.nonholic = holiton
            if 'organization' in request.POST:
                data.quota = request.POST['organization']
            else:
                data.quota = ''
            # data.miscInfo = helpers.getMiscInfo(form.cleaned_data)
            # Hack-around: not implemented yet
            data.member = False
            data.hasPaid = False
            data.event_type = temp
            data.save()
            return HttpResponseRedirect('/thanks/' + reserve)
    else:
        quotas = None
        can_signup = False
        signup_passed = False
        now = datetime.now(timezone.utc)
        participants = Participant.objects.filter(event_type=uid)
        if event.signup_starts is not None and event.signup_starts <= now:
            can_signup = True
        if event.signup_ends is not None and event.signup_ends <= now:
            signup_passed = True
        if event_type == 'sitsit':
            form = SitzSignupForm()
        elif event_type == 'vuosijuhlat':
            form = AnnualfestSignupForm()
        elif event_type == 'ekskursio':
            form = ExcursionSignupForm()
        elif event_type == 'muutapahtuma':
            form = OtherEventSignupForm()
        elif event_type == 'custom':
            form = CustomSignupForm()
    try:
        if len(event.quotas) > 0:
            quotas = helpers.get_quota_names(event.quotas, True)
    except AttributeError:
        pass
    return render(request, "eventsignup/signup.html",
                  {'form': form, 'event': event, 'quotas': quotas, 'cansignup': can_signup, 'signuppassed': signup_passed,
                   'page': 'Ilmoittaudu', 'participants': participants, 'baseurl': helpers.get_baseurl(request)})


# Arkistoi tapahtuman erilliseen arkistoon (säilyttää vain olennaisimmat tapahtuman tiedot.
# Poistaa tämän jälkeen varsinaisen tapahtuman kannasta osallistujineen.
# Arkisto on vain ylläpitäjien nähtävissä.
@login_required
def archive(request, uid):
    event = helpers.get_event(uid)
    archive_event = Archive(event_type=event.event_type, name=event.name, description=event.description,
                           participants=Participant.objects.filter(event_type=uid).count(), owner=event.owner,
                           date=event.date, place=event.place, pic=event.pic, prize=event.prize)
    archive_event.save()
    Events.objects.filter(uid=uid).delete()
    return render(request, "eventsignup/delete_success.html", {'baseurl': helpers.get_baseurl(request)})


# Tuottaa lomakeen uuden tapahtuman luomiseksi ja käsittelee sen.
@login_required
def add(request, **kwargs):
    desktop = True
    if 'Mobi' in request.META['HTTP_USER_AGENT']:
        desktop = False
    if kwargs:
        event_type = kwargs['type']
    if request.method == 'POST':
        uid = helpers.get_uid()
        form = helpers.get_form(event_type, request)
        if form.is_valid():
            User = get_user_model()
            event = Events(event_type, uid, request.user.get_username())
            event.save()
            data = form.save(commit=False)
            data.uid = Events.objects.get(uid=uid)
            data.event_type = EventType.objects.get(event_type=event_type)
            #            data.owner=EventOwner.objects.get(name=request.user.get_username())
            data.owner = User.objects.get(username=request.user.get_username())
            # data.description = data.description.replace("\n", "</p><p>")
            data.signup_starts = datetime.combine(form.cleaned_data['signup_starts_date'],
                                                  form.cleaned_data['signup_starts_time'], tzinfo=timezone.utc)
            if not (form.cleaned_data['signup_ends_date'] is None or form.cleaned_data['signup_ends_time'] is None):
                data.signup_ends = datetime.combine(form.cleaned_data['signup_ends_date'],
                                                    form.cleaned_data['signup_ends_time'], tzinfo=timezone.utc)
            else:
                data.signup_ends = None
            data.save()
            helpers.send_email(data, request)
            return HttpResponseRedirect('/event/' + str(uid) + '/preview/')
    else:
        if event_type == 'sitsit':
            form = SitzForm()
        elif event_type == 'vuosijuhlat':
            form = AnnualfestForm()
        elif event_type == 'ekskursio':
            form = ExcursionForm()
        elif event_type == 'muutapahtuma':
            form = OtherEventForm()
        elif event_type == 'custom':
            form = CustomForm()
    return render(request, "eventsignup/new_event.html",
                  {'form': form, 'edit': False, 'desktop': desktop, 'page': 'Lisää tapahtuma',
                   'baseurl': helpers.get_baseurl(request)})


# Lomake tapahtumatyypin valintaan ennen varsinaista lomaketta.
@login_required
def formtype(request, **kwargs):
    # sitsit, vujut, eksku, muu, custom
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'sitsit':
            return HttpResponseRedirect('/event/add/' + choice)
        elif choice == 'vuosijuhlat':
            return HttpResponseRedirect('/event/add/' + choice)
        elif choice == 'ekskursio':
            return HttpResponseRedirect('/event/add/' + choice)
        elif choice == 'muutapahtuma':
            return HttpResponseRedirect('/event/add/' + choice)
        elif choice == 'custom':
            return HttpResponseRedirect('/event/add/' + choice)
    else:
        form = SelectTypeForm()
    return render(request, "eventsignup/new_event.html",
                  {'form': form, 'choice': True, 'page': 'Lisää tapahtuma', 'baseurl': helpers.get_baseurl(request)})


# Näyttää tapahtuman tiedot ja osallistujalistan.
@login_required
def info(request, uid, **kwargs):
    if request.method == 'POST':
        Participant.objects.filter(event_type=uid, email=request.POST['user']).delete()
        return HttpResponseRedirect('/event/' + str(uid) + '/view/')
    else:
        just_list = False
        participants = Participant.objects.filter(event_type=uid)
        event = helpers.get_event(uid)
        if kwargs:
            if kwargs['type'] == 'list':
                just_list = True
        other = False
        export_options = helpers.get_export_options()
        return render(request, "eventsignup/view_event.html",
                      {'other': other, 'just_list': just_list, 'event': event, 'participants': participants,
                       'page': 'Tarkastele tapahtumaa', 'export_options': export_options,
                       'baseurl': helpers.get_baseurl(request)})


# Sisäänkirjautumisen jälkeen näytettävä "hallintapaneeli".
# Listaa sisäänkirjautuneen käyttäjän nykyiset ja menneet (ei arkistoidut) tapahtumat.
# Mahdollistaa myös niiden muokkauksen.
@login_required
def management(request):
    desktop = True
    if 'Mobi' in request.META['HTTP_USER_AGENT']:
        desktop = False
    participant_count = helpers.get_participant_count()
    auth_user = request.user.get_username()
    startdate = datetime.now()
    todaysdate = startdate.strftime("%Y-%m-%d")
    #
    #
    upcoming_sitz = Sitz.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_sitz = Sitz.objects.filter(date__lt=todaysdate, owner=auth_user)

    upcoming_other_events = OtherEvent.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_other_events = OtherEvent.objects.filter(date__lt=todaysdate, owner=auth_user)

    upcoming_excursion = Excursion.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_excursion = Excursion.objects.filter(date__lt=todaysdate, owner=auth_user)

    upcoming_annualfest = Annualfest.objects.filter(date__gte=todaysdate, owner=auth_user)
    previous_annualfest = Annualfest.objects.filter(date__lt=todaysdate, owner=auth_user)
    # eventit = list(chain(sitsit, ekskursiot, vujut, muut_tapahtumat))
    return render(request, "eventsignup/management.html",
                  {'menneet_sitsit': previous_sitz, 'tulevat_sitsit': upcoming_sitz,
                   'menneet_muutTapahtumat': previous_other_events, 'tulevat_muutTapahtumat': upcoming_other_events,
                   'menneet_ekskursiot': previous_excursion, 'tulevat_ekskursiot': upcoming_excursion,
                   'menneet_vujut': previous_annualfest, 'tulevat_vujut': upcoming_annualfest,
                   'baseurl': helpers.get_baseurl(request), 'osallistujamaarat': helpers.get_participant_count(),
                   'desktop': desktop, 'management': True,
                   }
                  )


# Olemassa olevan tapahtuman muokkaus.
@login_required
def edit(request, **kwargs):
    event = helpers.get_event(kwargs['uid'])
    form = helpers.get_editable_form(event)
    desktop = True
    if request.method == 'POST':
        form = helpers.get_form(event.event_type.event_type, request, initial=event)
        if form.is_valid():
            data = form.save(commit=False)
            data.signup_starts = datetime.combine(form.cleaned_data['signup_starts_date'],
                                                  form.cleaned_data['signup_starts_time'], tzinfo=timezone.utc)
            if not (form.cleaned_data['signup_ends_date'] is None or form.cleaned_data['signup_ends_time'] is None):
                data.signup_ends = datetime.combine(form.cleaned_data['signup_ends_date'],
                                                    form.cleaned_data['signup_ends_time'], tzinfo=timezone.utc)
            else:
                data.signup_ends = None
            data.save()
            helpers.send_email(data, request)
            return HttpResponseRedirect('/event/' + str(event.uid.uid) + '/preview/edit')
    else:
        if 'Mobi' in request.META['HTTP_USER_AGENT']:
            desktop = False
    return render(request, "eventsignup/new_event.html",
                  {'event': event, 'form': form, 'edit': True, 'page': 'Muokkaa tapahtumaa', 'desktop': desktop,
                   'baseurl': helpers.get_baseurl(request)})


# Uuden tapahtuman luonnin jälkeen näytettävä esikatselu.
@login_required
def preview(request, uid, **kwargs):
    #    url = reverse('home',urlconf='riskiwww.urls')+"eventsignup"
    event = helpers.get_event(uid)
    editing = False
    if kwargs and kwargs['type'] == 'edit':
        editing = True
    return render(request, "eventsignup/preview.html",
                  {'event': event, 'edit': editing, 'baseurl': helpers.get_baseurl(request)})


# Tapahtuman osallistujalistan exporttaus
@login_required
def export(request, uid, **kwargs):
    if request.method == 'POST' and len(request.POST) > 1:
        mimetypes.init()
        participants = Participant.objects.filter(event_type=uid).values()
        event = helpers.get_event(uid)
        type_of_export = None
        content_type = None
        list_of_exports = None
        # TODO parempi tarkistus eri export tyypeille
        if 'pdf' in request.POST and 'csv' in request.POST:
            type_of_export = 'zip'
            content_type = mimetypes.types_map['.zip']
            list_of_exports = ['csv', 'pdf']
        elif 'csv' in request.POST:
            type_of_export = "csv"
            content_type = mimetypes.types_map['.csv']
        elif 'pdf' in request.POST:
            type_of_export = 'pdf'
            content_type = mimetypes.types_map['.pdf']
        else:
            raise Http404
        with tempfile.TemporaryDirectory() as directory:
            file_name = helpers.gen_export(event, type_of_export, participants, list_of_exports, directory)
            if Path(directory + '/' + file_name).exists():
                with open(directory + '/' + file_name, 'rb') as f:
                    response = HttpResponse(f.read(), content_type=content_type)
                response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            else:
                raise Http404
        return response
    else:
        raise Http404
