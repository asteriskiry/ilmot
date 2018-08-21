from django.forms import ModelForm
from django import forms
from .models import Sitz, Annualfest, OtherEvent, Excursion, Participant
from .widgets import *

# Lomake sitsit-tyypille.
class SitzForm(ModelForm):
	quotas=forms.CharField(max_length=500,required=False,label='Järjestävien tahojen osallistujakiintiöt',help_text='Järjestö 1: lkm, Järjestö 2: lkm ...')
	class Meta:
		model = Sitz
		fields = '__all__'

# Lomake vuosijuhlat-tyypille.
class AnnualfestForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AnnualfestForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget = MyDateInput(attrs={'class':'date'})
		self.fields['start_time'].widget = MyTimeInput(attrs={'class':'date'})
		self.fields['signup_starts'].widget = MyDateTimeInput(attrs={'class':'date'})
		self.fields['signup_ends'].widget = MyDateTimeInput(attrs={'class':'date'})
	class Meta:
		model=Annualfest
		fields='__all__'

# Lomake muu-tyypille.
class OtherEventForm(ModelForm):
	class Meta:
		model=OtherEvent
		fields='__all__'

# Lomake ekskursio-tyypille.
class ExcursionForm(ModelForm):
	class Meta:
		model=Excursion
		fields='__all__'

# Lomake custom tapahtumalle.
class CustomForm(ModelForm):
	#tähän jotain kenttiä vielä!!!
	class Meta:
		model=OtherEvent
		fields='__all__'

# Osallistumislomake sitsit-tyypille.
class SitzSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

# Osallistumislomake vuosijuhlat-tyypille.
class AnnualfestSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi 1, Nimi 2, ...')
	class Meta:
		model=Participant
		fields=['name','email','lihaton','holiton','avec','plaseeraus']

# Osallistumislomake ekskursio-tyypille.
class ExcursionSignupForm(ModelForm):
	class Meta:
		model=Participant
		fields='__all__'

# Osallistumislomake muu-tyypille.
class OtherEventSignupForm(ModelForm):
	class Meta:
		model=Participant
		fields='__all__'

# Osallistumislomake custom-tyypille.
class CustomSignupForm(ModelForm):
	class Meta:
		model=Participant
		fields='__all__'

# Tapahtumatyypin valintalomake.
class SelectTypeForm(forms.Form):
	choice=forms.ChoiceField(label='Tapahtuman tyyppi',help_text='Valmiiksi määritellyillä tyypeillä tulee kyseiseen tapahtumaan soveltuva lomake. "Mukautettu" valinnalla voit mukauttaa tiedot haluamallasi tavalla.',choices=(('sitsit','Sitsit'),('vuosijuhlat','Vuosijuhlat'),('ekskursio','Ekskursio'),('muutapahtuma','Muu tapahtuma'),('custom','Mukautettu')))

