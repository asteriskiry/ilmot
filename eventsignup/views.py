from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

# Create your views here.
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from .models import EventType, EventOwner, Events, Participant, Sitz, Annualfest, Excursion, OtherEvent
#from django import forms
from eventsignup.forms import AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
from eventsignup.forms import SitzSignupForm, AnnualfestSignupForm, ExcursionSignupForm, OtherEventSignupForm, CustomSignupForm
from omat import helpers

def index(request):
	return render(request, "eventsignup/index.html")

def thanks(request):
	return render(request, "eventsignup/thankyou.html")


#sivupaneelin nippelitieto
@login_required
def stats(request, uid):
	pass

def signup(request, uid):
	temp=Events.objects.get(uid=uid)
	event_type=temp.event_type.event_type
	if(request.method == 'POST'):
		form=helpers.getSignupForm(event_type,request)
		if(form.is_valid()):
			#käsittele lomake
			data=form.save(commit=False)
			data.miscInfo=helpers.getMiscInfo(request.POST)
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
		if(event.quotas is not None):
			quotas=helpers.getQuotaNames(event.quotas)
	except AttributeError:
		pass
	return render(request, "eventsignup/signup.html", {'form': form, 'event':event, 'quotas':quotas} )

@login_required
def archive(request, uid):
	pass

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

@login_required
def management(request):
	#eventit = Events.objects.all()

	sitsit = Sitz.objects.filter(owner=request.user.get_username())
	ekskursiot = Excursion.objects.filter(owner=request.user.get_username())
	muut_tapahtumat = OtherEvent.objects.filter(owner=request.user.get_username())
	vujut = Annualfest.objects.filter(owner=request.user.get_username())
	eventit = list(chain(sitsit, ekskursiot, vujut, muut_tapahtumat))
	return render(request, "eventsignup/management.html", {'eventit':eventit})

@login_required
def edit(request):
	pass

@login_required
def preview(request, uid):
	event=helpers.getEvent(uid)
	return render(request, "eventsignup/preview.html", {'event': event,'baseurl':'http://212.32.242.196:7777/eventsignup'})
