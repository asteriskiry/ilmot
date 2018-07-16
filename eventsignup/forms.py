from django.forms import ModelForm
from django import forms
from .models import Sitsit, Vuosijuhla, MuuTapahtuma, Ekskursio, Osallistuja

class SitzForm(ModelForm):
	class Meta:
		model = Sitz
		fields = '__all__'

class AnnualfestForm(ModelForm):
	class Meta:
		model=Annualfest
		fields='__all__'

class OtherEventForm(ModelForm):
	class Meta:
		model=OtherEvent
		fields='__all__'

class ExcursionForm(ModelForm):
	class Meta:
		model=Excursion
		fields='__all__'

class CustomForm(ModelForm):
	#tähän jotain kenttiä vielä!!!
	class Meta:
		model=OtherEvent
		fields='__all__'

class SitzSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

class SelectTypeForm(forms.Form):
	choice=forms.ChoiceField(label='Tapahtuman tyyppi',help_text='Valmiiksi määritellyillä tyypeillä tulee kyseiseen tapahtumaan soveltuva lomake. "Mukautettu" valinnalla voit mukauttaa tiedot haluamallasi tavalla.',choices=(('sitsit','Sitsit'),('vujut','Vuosijuhlat'),('eksku','Ekskursio'),('muu','Muu tapahtuma'),('custom','Mukautettu')))
