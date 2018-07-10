from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import TapahtumaTyypit, TapahtumanOmistaja, Tapahtumat, Sitsit, Vuosijuhla, Ekskursio
from .models import MuuTapahtuma, Osallistuja, Arkisto

def index(request):
	return HttpResponse("Welcome!")

def stats(request, uid):
	pass

def signup(request, uid, **kwargs):
	pass

def archive(request, uid):
	pass

def new(request, **kwargs):
	pass

def info(request, uid):
	pass
