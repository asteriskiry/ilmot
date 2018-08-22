from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

from django.http import HttpResponseRedirect, HttpResponse
from .models import EventType, EventOwner, Events, Sitz, Annualfest, Excursion, OtherEvent
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
from omat import helpers
from datetime import datetime, timezone

# Koko järjestelmän juuri (= /) sivu.
def index(request):
	return render(request, "eventsignup/index.html")

# Tapahtumaan ilmoittautumisen jälkeen näytettävä kiitossivu.
def thanks(request):
	# refereristä uid, jotta event.name ja owner.email saadaan tietokannasta.
	event=None
	temp=request.META['HTTP_REFERER'].split("/")
	try:
		for x in temp:
			if(str.isdigit(x)):
				uid=int(x)
#		uid=''.join(filter(str.isdigit, request.META['HTTP_REFERER']))
		event=helpers.getEvent(uid)
	except KeyError:
		pass
	except OverflowError:
		pass
	return render(request, "eventsignup/thankyou.html",{'event':event})

# GDPR/tietosuojatiedot
def privacy(request):
	return render(request, "eventsignup/privacy.html")

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
		canSignup=False
		signupPassed=False
		now=datetime.now(timezone.utc)
		if(event.signup_starts is not None and event.signup_starts<=now):
			canSignup=True
		if(event.signup_ends is not None and event.signup_ends<=now):
			signupPassed=True
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
	return render(request, "eventsignup/signup.html", {'form': form, 'event':event, 'quotas':quotas, 'cansignup':canSignup, 'signuppassed':signupPassed,'page':'Ilmoittaudu'} )

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
			event=Events(event_type,uid,request.user.get_username())
			event.save()
			data=form.save(commit=False)
			data.uid=Events.objects.get(uid=uid)
			data.event_type=EventType.objects.get(event_type=event_type)
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
	return render(request,"eventsignup/new_event.html",{'form':form,'desktop':False,'page':'Lisää tapahtuma','baseurl':helpers.getBaseurl(request)})

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
	return render(request, "eventsignup/new_event.html", {'form': form,'choice':True,'page':'Lisää tapahtuma','baseurl':helpers.getBaseurl(request)})

@login_required
def info(request, uid):
	pass

# Sisäänkirjautumisen jälkeen näytettävä "hallintapaneeli".
# Listaa sisäänkirjautuneen käyttäjän nykyiset ja menneet (ei arkistoidut) tapahtumat.
# Mahdollistaa myös niiden muokkauksen.
@login_required
def management(request):
	#eventit = Events.objects.all()

	sitsit = Sitz.objects.filter(owner=request.user.get_username())
	ekskursiot = Excursion.objects.filter(owner=request.user.get_username())
	muut_tapahtumat = OtherEvent.objects.filter(owner=request.user.get_username())
	vujut = Annualfest.objects.filter(owner=request.user.get_username())
	eventit = list(chain(sitsit, ekskursiot, vujut, muut_tapahtumat))
	return render(request, "eventsignup/management.html", {'eventit':eventit})

# Olemassa olevan tapahtuman muokkaus.
@login_required
def edit(request, **kwargs):
	if(kwargs['type']=='signups'):
		return HttpResponse('Editing signups list')
	elif(kwargs['type']=='event'):
		return HttpResponse('Editing event itself')
	else:
		return HttpResponseRedirect('eventsignup/management/')

# Uuden tapahtuman luonnin jälkeen näytettävä esikatselu.
@login_required
def preview(request, uid):
	event=helpers.getEvent(uid)
	return render(request, "eventsignup/preview.html", {'event': event,'baseurl':helpers.getBaseurl(request)})

