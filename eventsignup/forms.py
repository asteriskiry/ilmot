from django.forms import ModelForm
from .models import Sitsit, Vuosijuhla, MuuTapahtuma, Ekskursio

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
