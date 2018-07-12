from django.db import models

# Create your models here.
class TapahtumaTyypit(models.Model):
	tyyppi=models.CharField(max_length=500,unique=True, verbose_name='Tapahtuman tyyppi')
	def __str__(self):
		return "Tapahtuman typpi: "+self.tyyppi

class TapahtumanOmistaja(models.Model):
	nimi=models.CharField(max_length=500, unique=True, verbose_name='Järjestävä taho')
	def __str__(self):
		return "Tapahtuman järjestäjä(t): "+self.nimi

class Tapahtumat(models.Model):
	tyyppi=models.ForeignKey(TapahtumaTyypit, on_delete=models.CASCADE)
	uid=models.PositiveIntegerField(primary_key=True)
	omistaja=models.ForeignKey(TapahtumanOmistaja, on_delete=models.CASCADE)
	def __str__(self):
		return "Tapahtuman tyyppi: "+self.typpi+", uid: "+self.uid+", tapahtuman järjestäjä(t): "+self.omistaja

class CommonInfo(models.Model):
	#kaikki yhteiset attribuutit tähän
	uid=models.ForeignKey(Tapahtumat, on_delete=models.CASCADE,editable=False)
	tyyppi=models.ForeignKey(TapahtumaTyypit, on_delete=models.CASCADE,editable=False)
	omistaja=models.ForeignKey(TapahtumanOmistaja, on_delete=models.CASCADE,editable=False)
	nimi=models.CharField(max_length=500, verbose_name='Tapahtuman nimi')
	paikka=models.CharField(max_length=200, verbose_name='Pitopaikka')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	kuvaus=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	kuva=models.ImageField(blank=True, null=True,verbose_name='Ilmoittautumislomakkeen kansikuva')
	hinta=models.CharField(max_length=500,blank=True, null=True,verbose_name='Tapahtuman hinta')
	max_osallistujia=models.PositiveIntegerField(blank=True, null=True,verbose_name='Maksimimäärä osallistujia')
	ilmo_alkaa=models.DateTimeField(verbose_name='Tapahtumaan ilmoittautuminen avautuu')
	ilmo_loppuu=models.DateTimeField(blank=True, null=True,verbose_name='Tapahtumaan ilmoittautuminen sulkeutuu')

	def __str__(self):
		return "Tapahtuman järjestäjä: "+self.omistaja+", Tapahtuman tyyppi: "+self.tyyppi+", Tapahtuman nimi: "+self.nimi+", Pitopaikka "+self.paikka+", Hinta: "+self.hinta+", Tapahtuman pitopäivä: "+self.date+", Maksimi osallistujamäärä: "+self.max_osallistujia+", Ilmoittautuminen alkaa: "+self.ilmo_alkaa+", Ilmoittautuminen loppuu: "+self.ilmo_loppuu+", Yleiskuvaus: "+self.kuvaus

	class Meta:
		abstract = True

class Sitsit(CommonInfo):
	quotas=models.CharField(max_length=500,null=True, blank=True,verbose_name='Järjestävien tahojen osallistujakiintiöt')
#	avec=models.CharField(max_length=500,blank=True)
#	plaseerustoive=models.CharField(max_length=500,blank=True)
	def __str__(self):
		return super().__str__()+", Osallistujakiintiöt: "+self.quotas

class Vuosijuhla(CommonInfo):
#	avec=models.CharField(max_length=500,blank=True)
#	plaseerustoive=models.CharField(max_length=500,blank=True)
	def __str__(self):
		return super().__str__()

class Ekskursio(CommonInfo):
	date=models.DateField(verbose_name='Ekskursion aloituspäivä')
	end_date=models.DateField(verbose_name='Ekskursion loppumispäivä')
	def __str__(self):
		return super().__str__()+", Päättymispäivä: "+self.end_date

class MuuTapahtuma(CommonInfo):
	min_osallistujia=models.PositiveIntegerField(blank=True, null=True,verbose_name='Minimimäärä osallistujia')
	def __str__(self):
		return super().__str__()+", Minimimäärä osallistujia: "+self.min_osallistujia

class Osallistuja(models.Model):
	tapahtuma=models.ForeignKey(Tapahtumat, on_delete=models.CASCADE,editable=False)
	nimi=models.CharField(max_length=200)
	email=models.EmailField(verbose_name='Sähköpostiosoite')
#	lihaton=models.NullBooleanField()
#	holiton=models.NullBooleanField()
#	is_member=models.NullBooleanField()
#	has_paid=models.NullBooleanField()
#
#	Tämä kenttä sisältää tiedot: holillinen/holiton, liha/kasvis, jäsen/ei jäsen, onko maksanut, avec, plaseeraustoive.
#	datan tulee olla muodossa {lihaton: arvo, holiton:arvo, member:arvo, hasPaid:arvo, avec:arvo, plaseeraus:arvo}
	miscInfo=models.TextField(editable=False)
	def __str__(self):
		return self.nimi+" ("+self.email+"), muut tiedot: "+self.miscInfo

class Arkisto(models.Model):
	tyyppi=models.CharField(max_length=500,verbose_name='Tapahtuman typpi')
	nimi=models.CharField(max_length=500,verbose_name='Tapahtuman nimi')
	kuvaus=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	participants=models.IntegerField(verbose_name='Osallistujamäärä')
	omistaja=models.CharField(max_length=500,verbose_name='Tapahtuman pitäjä')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	def __str__(self):
		return "Tapahtuman tyyppi: "+self.tyyppi+", Tapahtuman nimi: "+self.nimi+", Kokonaisosallistujamäärä: "+self.participants+", Tapahtuman järjestäjä: "+self.omistaja+",Alkuperäinen pitopäivä: "+self.date", Yleiskuvaus: "+self.kuvaus

