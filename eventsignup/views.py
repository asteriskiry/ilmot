from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from .models import EventType, EventOwner, Events, Sitz, Annualfest, Excursion
from .models import OtherEvent, Participant
#from django import forms
from eventsignup.forms import SitzSignupForm, AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
from omat import helpers

def index(request):
	#kts tutoriaali!! template tms
	#return render(request,'eventsignup/info.html',{'info':info})
#	form = SitzSignupForm()
	return render(request, "eventsignup/index.html")
	#return HttpResponse("Welcome!")

#sivupaneelin nippelitieto
@login_required
def stats(request, uid):
	pass

def signup(request, uid):
	#return HttpResponse(filter(str.isdigit, request.path))
	return HttpResponse(uid)
#	if(request.method == 'POST'):
		#tee jotain
#		tyyppi=get_object_or_404(Tapahtumat, uid=uid)
#		form = SitsitSignupForm(request.POST)
#		if(form.is_valid()):
			#käsittele lomake
#	else:
#		event= jotain
#		form = SitsitSignupForm()
#	return render(request, "eventsignup/new_event.html", {'form': form}, {'event':event} )

@login_required
def archive(request, uid):
	pass

#@login_required
def add(request,**kwargs):
	if kwargs:
		event_type=kwargs['type']
	if(request.method=='POST'):
		uid=helpers.getUid()
		#käsittele lomake
		form=helpers.getForm(event_type,request)
		if form.is_valid():
			#tee jotain
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
	return render(request,"eventsignup/new_event.html",{'form':form})

#@login_required
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
	return render(request, "eventsignup/new_event.html", {'form': form})

@login_required
def info(request, uid):
	pass

#@login_required
def management(request):
	return render(request, "eventsignup/management.html")

@login_required
def edit(request):
	pass

#@login_required
def preview(request, uid):
	event=helpers.getEvent(uid)
	return render(request, "eventsignup/preview.html", {'event': event})
