from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
#from .models import TapahtumaTyypit, TapahtumanOmistaja, Tapahtumat, Sitsit, Vuosijuhla, Ekskursio
#from .models import MuuTapahtuma, Osallistuja, Arkisto
from django import forms
from eventsignup.forms import MuuTapahtumaForm

def index(request):
	#kts tutoriaali!! template tms
	#return render(request,'eventsignup/info.html',{'info':info})
	form = MuuTapahtumaForm()
	return render(request, "eventsignup/test_template.html", {'form': form})
	#return HttpResponse("Welcome!")

def stats(request, uid):
	pass

def signup(request, uid, **kwargs):
	pass

def archive(request, uid):
	pass

def add(request):
	return render(request,'eventsignup/addNewForm.html')

def formtype(request,eventtype):
	pass

def new(request, **kwargs):
	pass

def info(request, uid):
	pass
