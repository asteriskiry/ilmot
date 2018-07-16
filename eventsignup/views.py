from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse
#from .models import TapahtumaTyypit, TapahtumanOmistaja, Tapahtumat, Sitsit, Vuosijuhla, Ekskursio
#from .models import MuuTapahtuma, Osallistuja, Arkisto
#from django import forms
from eventsignup.forms import SitsitSignupForm, VuosijuhlaForm, EkskursioForm, MuuTapahtumaForm, CustomForm, SelectTypeForm, SitsitForm
#from omat import helpers
import random

def index(request):
	#kts tutoriaali!! template tms
	#return render(request,'eventsignup/info.html',{'info':info})
	form = SitsitSignupForm()
	return render(request, "eventsignup/new_event.html", {'form': form})
	#return HttpResponse("Welcome!")

#sivupaneelin nippelitieto
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
#		form = SitsitSignupForm()
#	return render(request, "eventsignup/new_event.html", {'form': form})

def archive(request, uid):
	pass

def add(request,**kwargs):
	if kwargs:
		return HttpResponse(kwargs['type'])
	if(request.method=='POST'):
		uid=random.randint(10000, 99999)
		#käsittele lomake
		form=SelectTypeForm()
	else:
		form=SelectTypeForm()
	return render(request,"eventsignup/new_event.html",{'form':form})

def formtype(request,eventtype):
#	sitsit, vujut, eksku, muu, custom
	if(request.method=='POST'):
		return HttpResponseNotAllowed(['GET',''])
	if(eventtype=='sitsit'):
		form = SitsitForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='vujut'):
		form = VuosijuhlaForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='eksku'):
		form = EkskursioForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='muu'):
		form = MuuTapahtumaForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='custom'):
		form = CustomForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	else:
		return HttpResponseBadRequest()

def info(request, uid):
	pass
