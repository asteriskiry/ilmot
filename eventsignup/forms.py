from django.forms import ModelForm
from django import forms
from .models import Sitsit, Vuosijuhla, MuuTapahtuma, Ekskursio, Osallistuja

class SitsitForm(ModelForm):
	class Meta:
		model = Sitsit
		fields = '__all__'

class VuosijuhlaForm(ModelForm):
	class Meta:
		model=Vuosijuhla
		fields='__all__'

class MuuTapahtumaForm(ModelForm):
	class Meta:
		model=MuuTapahtuma
		fields='__all__'

class EkskursioForm(ModelForm):
	class Meta:
		model=Ekskursio
		fields='__all__'

#class SitsitSignupForm(forms.Form):
#	nimi=forms.charField(label='Nimi')
#	email=forms.emailField(label='Sähköpostiosoite')
#	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu')
#	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu')
#	avec=forms.charField(required=False,label='Avec')
#	plaseeraus=forms.charField(required=False,label='Plaseeraustoive')

class SitsitSignupForm(ModelForm):
	holiton=forms.ChoiceField(label='Holillinen/Holiton Menu',choices=(('holillinen','Alkoholillinen'),('holiton','Alkoholiton')))
	lihaton=forms.ChoiceField(label='Liha/Kasvis Menu',choices=(('liha','Liha'),('kasvis','Kasvis')))
	avec=forms.CharField(required=False,label='Avec',help_text='Jätä tyhjäksi, jos ei ole.')
	plaseeraus=forms.CharField(required=False,label='Plaseeraustoive',help_text='Nimi1, Nimi2, ...')
	class Meta:
		model=Osallistuja
		fields=['nimi','email','lihaton','holiton','avec','plaseeraus']

