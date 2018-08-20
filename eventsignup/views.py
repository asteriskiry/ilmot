from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from itertools import chain
import datetime

# Create your views here.
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from .models import EventType, EventOwner, Events, Participant, Sitz, Annualfest, Excursion, OtherEvent
#from django import forms
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
from omat import helpers

# Koko järjestelmän juuri (= /) sivu.
def index(request):
	return render(request, "eventsignup/index.html")

# Tapahtumaan ilmoittautumisen jälkeen näytettävä kiitossivu.
def thanks(request):
	return render(request, "eventsignup/thankyou.html")


# Tuottaa ja palauttaa oikeaann sivupaneeliin tulevat widgetin nippelitiedot.
@login_required
def stats(request, uid):
	pass

# Tuottaa ilmoittautumislomakkeen uid:tä vastaavaan tapahtumaan.
# Käsittelee ja tallentaa lomakkeelta tulevan ilmoittautumisen.
def signup(request, uid):
	temp=Events.objects.get(uid=uid)
	event_type=temp.event_type.event_type
	if(request.method == 'POST'):
		form=helpers.getSignupForm(event_type,request)
		if(form.is_valid()):
			#käsittele lomake
			data=form.save(commit=False)
			data.miscInfo=helpers.getMiscInfo(form.cleaned_data)
			data.event_type=temp
			data.save()
			return HttpResponseRedirect('/eventsignup/thanks')
	else:
		event=helpers.getEvent(uid)
		quotas=None
		if(event_type=='sitsit'):
			form = SitzSignupForm()
		elif(event_type=='vuosijuhlat'):
			form = AnnualfestSignupForm()
		elif(event_type=='ekskursio'):
			form = ExcursionSignupForm()
		elif(event_type=='muutapahtuma'):
			form = OtherEventSignupForm()
		elif(event_type=='custom'):
			form = CustomSignupForm()
	try:
		if(len(event.quotas)>0):
			quotas=helpers.getQuotaNames(event.quotas)
	except AttributeError:
		pass
	return render(request, "eventsignup/signup.html", {'form': form, 'event':event, 'quotas':quotas} )

# Arkistoi tapahtuman erilliseen arkistoon (säilyttää vain olennaisimmat tapahtuman tiedot.
# Poistaa tämän jälkeen varsinaisen tapahtuman kannasta osallistujineen.
# Arkisto on vain ylläpitäjien nähtävissä.
@login_required
def archive(request, uid):
	pass

# Tuottaa lomakeen uuden tapahtuman luomiseksi ja käsittelee sen.
@login_required
def add(request,**kwargs):
	desktop=True
#	if('Mobi'in request.META['HTTP_USER_AGENT']):
#		desktop=False
	if kwargs:
		event_type=kwargs['type']
	if(request.method=='POST'):
		uid=helpers.getUid()
		form=helpers.getForm(event_type,request)
		if form.is_valid():
			#tee jotain
#			event=Events()
#			if request.user.is_authenticated:
			event=Events(event_type,uid,request.user.get_username())
#			else:
				#eventType=EventType.objects.get(event_type='sitz')
				#eventOwner=EventOwner.objects.get(name='test')
#				event=Events(EventType.objects.get(event_type='sitz'),uid,EventOwner.objects.get(name='test'))
#				event.uid=uid
#				event.event_type=EventType.objects.get(event_type='sitz')
#				event.owner=EventOwner.objects.get(name='test')
#			event.uid=uid
			event.save()
			data=form.save(commit=False)
			data.uid=Events.objects.get(uid=uid)
			data.event_type=EventType.objects.get(event_type=event_type)
#			data.owner=EventOwner.objects.get(name='test')
			data.owner=EventOwner.objects.get(name=request.user.get_username())
			data.save()
			helpers.sendEmail(data,request)
			return HttpResponseRedirect('/eventsignup/event/'+str(uid)+'/preview/')
	else:
		if(event_type=='sitsit'):
			form = SitzForm()
		elif(event_type=='vuosijuhlat'):
			form = AnnualfestForm()
		elif(event_type=='ekskursio'):
			form = ExcursionForm()
		elif(event_type=='muutapahtuma'):
			form = OtherEventForm()
		elif(event_type=='custom'):
			form = CustomForm()
	return render(request,"eventsignup/new_event.html",{'form':form,'desktop':desktop})

# Lomake tapahtumatyypin valintaan ennen varsinaista lomaketta.
@login_required
def formtype(request,**kwargs):
#	sitsit, vujut, eksku, muu, custom
	if(request.method=='POST'):
		temp=request.POST.get('choice')
		if(temp=='sitsit'):
			return HttpResponseRedirect('/eventsignup/event/add/'+temp)
		elif(temp=='vuosijuhlat'):
			return HttpResponseRedirect('/eventsignup/event/add/'+temp)
		elif(temp=='ekskursio'):
			return HttpResponseRedirect('/eventsignup/event/add/'+temp)
		elif(temp=='muutapahtuma'):
			return HttpResponseRedirect('/eventsignup/event/add/'+temp)
		elif(temp=='custom'):
			return HttpResponseRedirect('/eventsignup/event/add/'+temp)
	else:
		form=SelectTypeForm()
	return render(request, "eventsignup/new_event.html", {'form': form,'choice':True})

@login_required
def info(request, uid):
	pass

# Sisäänkirjautumisen jälkeen näytettävä "hallintapaneeli".
# Listaa sisäänkirjautuneen käyttäjän nykyiset ja menneet (ei arkistoidut) tapahtumat.
# Mahdollistaa myös niiden muokkauksen.
@login_required
def management(request):
	#eventit = Events.objects.all()
	url = reverse('home',urlconf='riskiwww.urls')+"eventsignup"
	auth_user= request.user.get_username()
	startdate = datetime.datetime.now()
	todaysdate =startdate.strftime("%Y-%m-%d")
	upcoming_sitz = Sitz.objects.filter(date__gte=todaysdate, owner=auth_user)
	previous_sitz = Sitz.objects.filter(date__lt=todaysdate, owner=auth_user)
	
	upcoming_otherEvents= OtherEvent.objects.filter(date__gte=todaysdate, owner=auth_user)
	previous_otherEvents = OtherEvent.objects.filter(date__lt=todaysdate, owner=auth_user)

	upcoming_excursion= Excursion.objects.filter(date__gte=todaysdate, owner=auth_user)
	previous_excursion = Excursion.objects.filter(date__lt=todaysdate, owner=auth_user)

	upcoming_annualfest= Annualfest.objects.filter(date__gte=todaysdate, owner=auth_user)
	previous_annualfest = Annualfest.objects.filter(date__lt=todaysdate, owner=auth_user)
	#eventit = list(chain(sitsit, ekskursiot, vujut, muut_tapahtumat))
	return render(request, "eventsignup/management.html",
	{'menneet_sitsit': previous_sitz, 'tulevat_sitsit': upcoming_sitz,
	 'menneet_muutTapahtumat': previous_otherEvents, 'tulevat_muutTapahtumat': upcoming_otherEvents,
	  'menneet_ekskursiot': previous_excursion, 'tulevat_ekskursiot': upcoming_excursion,
	   'menneet_vujut': previous_annualfest, 'tulevat_vujut': upcoming_annualfest,
	   'baseurl':url
	  }
	 )

# Olemassa olevan tapahtuman muokkaus.
@login_required
def edit(request):
	pass

# Uuden tapahtuman luonnin jälkeen näytettävä esikatselu.
@login_required
def preview(request, uid):
	url = reverse('home',urlconf='riskiwww.urls')+"eventsignup"
	event=helpers.getEvent(uid)
	return render(request, "eventsignup/preview.html", {'event': event,'baseurl':url})
