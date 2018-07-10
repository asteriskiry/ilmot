from django.db import models

# Create your models here.
class TapahtumaTyypit(models.Model):
	tyyppi=models.CharField(unique=True, verbose_name='Tapahtuman tyyppi')
	def __str__(self):
		return ""

class TapahtumanOmistaja(models.Model):
	nimi=models.CharField(max_length=500, unique=True, verbose_name='Järjestävä taho')
	def __str__(self):
		return ""

class Tapahtumat(models.Model):
	tyyppi=models.ForeignKey(TapahtumaTyypit, on_delete=models.CASCADE)
	uid=models.PositiveIntegerField(primary_key=True)
	omistaja=models.ForeignKey(TapahtumanOmistaja, on_delete=models.CASCADE)

class CommonInfo(models.Model):
	#kaikki yhteiset attribuutit tähän
	uid=models.ForeignKey(Tapahtumat, on_delete=models.CASCADE)
	tyyppi=models.ForeignKey(TapahtumaTyypit, on_delete=models.CASCADE)
	omistaja=models.ForeignKey(TapahtumanOmistaja, on_delete=models.CASCADE)
	nimi=models.CharField(max_length=500, verbose_name='Tapahtuman nimi')
	paikka=models.CharField(max_length=200, verbose_name='Pitopaikka')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	kuvaus=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	kuva=models.ImageField(blank=True, null=True)
	hinta=models.CharField(blank=True, null=True)
	max_osallistujia=models.PositiveIntegerField(blank=True, null=True)
	ilmo_alkaa=models.DateField()
	ilmo_loppuu=models.DateField(blank=True, null=True)
	class Meta:
		abstract = True

class Sitsit(CommonInfo):
	quotas=models.CharField(null=True, blank=True)
	avec=models.CharField(blank=True)
	plaseerustoive=models.CharField(blank=True)
	def __str__(self):
		return ""

class Vuosijuhla(CommonInfo):
	avec=models.CharField(blank=True)
	plaseerustoive=models.CharField(blank=True)
	def __str__(self):
		return ""

class Ekskursio(CommonInfo):
	start_date=models.DateField(null=True)
	end_date=models.DateField()
	def __str__(self):
		return ""

class MuuTapahtuma(CommonInfo):
	min_osallistujia=models.PositiveIntegerField(blank=True, null=True)
	def __str__(self):
		return ""

class Osallistuja(models.Model):
	tapahtuma=models.ForeignKey(Tapahtumat, on_delete=models.CASCADE)
	nimi=models.CharField(max_length=200)
	email=models.EmailField()
#	lihaton=models.NullBooleanField()
#	holiton=models.NullBooleanField()
#	is_member=models.NullBooleanField()
#	has_paid=models.NullBooleanField()
#
#	Tämä kenttä sisältää tiedot: holillinen/holiton, liha/kasvis, jäsen/ei jäsen, onko maksanut, avec, plaseeraustoive.
#	datan tulee olla muodossa {lihaton: arvo, holiton:arvo, member:arvo, hasPaid:arvo, avec:arvo, plaseeraus:arvo}
	miscInfo=models.CharField()
	def __str__(self):
		return ""

class Arkisto(models.Model):
	tyyppi=models.CharField(verbose_name='Tapahtuman typpi')
	nimi=models.CharField(verbose_name='Tapahtuman nimi')
	kuvaus=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	participants=models.IntegerField(verbose_name='Osallistujamäärä')
	omistaja=models.CharField(verbose_name='Tapahtuman pitäjä')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	def __str__(self):
		return ""

