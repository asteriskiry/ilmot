from django.forms import ModelForm
from django import forms
from .models import Sitz, Annualfest, OtherEvent, Excursion, Participant
from .widgets import *

class SitzForm(ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(SitzForm, self).__init__(*args, **kwargs)
#		self.fields['date'].widget = MyDateInput(attrs={'class':'date'})
#		self.fields['signup_starts'].widget = MyDateTimeInput(attrs={'class':'date'})
#		self.fields['signup_ends'].widget = MyDateTimeInput(attrs={'class':'date'})
	quotas=forms.CharField(max_length=500,required=False,label='Järjestävien tahojen osallistujakiintiöt',help_text='Järjestö 1: lkm, Järjestö 2: lkm ...')
	class Meta:
		model = Sitz
		fields = '__all__'

class AnnualfestForm(ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(AnnualfestForm, self).__init__(*args, **kwargs)
#		self.fields['date'].widget = MyDateInput(attrs={'class':'date'})
#		self.fields['signup_starts'].widget = MyDateTimeInput(attrs={'class':'date'})
#		self.fields['signup_ends'].widget = MyDateTimeInput(attrs={'class':'date'})
	class Meta:
		model=Annualfest
		fields='__all__'

class OtherEventForm(ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(OtherEventForm, self).__init__(*args, **kwargs)
#		self.fields['date'].widget = MyDateInput(attrs={'class':'date'})
#		self.fields['signup_starts'].widget = MyDateTimeInput(attrs={'class':'date'})
#		self.fields['signup_ends'].widget = MyDateTimeInput(attrs={'class':'date'})
	class Meta:
		model=OtherEvent
		fields='__all__'

class ExcursionForm(ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(ExcursionForm, self).__init__(*args, **kwargs)
#		self.fields['date'].widget = MyDateInput(attrs={'class':'date'})
#		self.fields['end_date'].widget = MyDateInput(attrs={'class':'date'})
#		self.fields['signup_starts'].widget = MyDateTimeInput(attrs={'class':'date'})
#		self.fields['signup_ends'].widget = MyDateTimeInput(attrs={'class':'date'})
#		self.fields['passenger_count'].widget = MyNumberInput(attrs={'min':0})
#		self.fields['email'].widget = MyEmailInput()

	class Meta:
		model=Excursion
		fields='__all__'

class CustomForm(ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(CustomForm, self).__init__(*args, **kwargs)
#		self.fields['date'].widget = MyDateInput(attrs={'class':'date'})
#		self.fields['signup_starts'].widget = MyDateTimeInput(attrs={'class':'date'})
#		self.fields['signup_ends'].widget = MyDateTimeInput(attrs={'class':'date'})
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

class AnnualfestSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

class ExcursionSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

class OtherEventSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

class CustomSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

class SelectTypeForm(forms.Form):
	choice=forms.ChoiceField(label='Tapahtuman tyyppi',help_text='Valmiiksi määritellyillä tyypeillä tulee kyseiseen tapahtumaan soveltuva lomake. "Mukautettu" valinnalla voit mukauttaa tiedot haluamallasi tavalla.',choices=(('sitsit','Sitsit'),('vuosijuhlat','Vuosijuhlat'),('ekskursio','Ekskursio'),('muutapahtuma','Muu tapahtuma'),('custom','Mukautettu')))
