from django.db import models

# Create your models here.
class EventType(models.Model):
	event_type=models.CharField(max_length=500,unique=True, verbose_name='Tapahtuman tyyppi')
	def __str__(self):
		return "Tapahtuman tyyppi: "+str(self.event_type)

class EventOwner(models.Model):
	name=models.CharField(max_length=500, unique=True, verbose_name='Järjestävä taho')
	def __str__(self):
		return "Tapahtuman järjestäjä(t)self.name: "+str(self.name)

class Events(models.Model):
	event_type=models.ForeignKey(EventType, to_field='event_type' ,on_delete=models.CASCADE)
	uid=models.PositiveIntegerField(primary_key=True)
	owner=models.ForeignKey(EventOwner, to_field='name', on_delete=models.CASCADE)
	def __str__(self):
		return "Tapahtuman tyyppi: "+str(self.event_type)+", uid: "+str(self.uid)+", tapahtuman järjestäjä(t) owner: "+str(self.owner)

class CommonInfo(models.Model):
	#kaikki yhteiset attribuutit tähän
	uid=models.ForeignKey(Events, on_delete=models.CASCADE,editable=False)
	event_type=models.ForeignKey(EventType, to_field='event_type', on_delete=models.CASCADE,editable=False)
	owner=models.ForeignKey(EventOwner, to_field='name', on_delete=models.CASCADE,editable=False)
	name=models.CharField(max_length=500, verbose_name='Tapahtuman nimi')
	place=models.CharField(max_length=200, verbose_name='Pitopaikka')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	start_time=models.TimeField(verbose_name='Tapahtuman alkamisaika', default='00:00:00')
	description=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	pic=models.ImageField(blank=True, null=True,verbose_name='Ilmoittautumislomakkeen kansikuva')
	prize=models.CharField(max_length=500,blank=True, null=True,verbose_name='Tapahtuman hinta')
	max_participants=models.PositiveIntegerField(blank=True, null=True,verbose_name='Maksimimäärä osallistujia')
	signup_starts=models.DateTimeField(verbose_name='Tapahtumaan ilmoittautuminen avautuu')
	signup_ends=models.DateTimeField(blank=True, null=True,verbose_name='Tapahtumaan ilmoittautuminen sulkeutuu')

	def __str__(self):
		return "Tapahtuman järjestäjä: "+str(self.owner)+", Tapahtuman tyyppi: "+str(self.event_type)+", Tapahtuman nimi: "+self.name+", Pitopaikka "+self.place+", Hinta: "+str(self.prize)+", Tapahtuman pitopäivä: "+str(self.date)+", Maksimi osallistujamäärä: "+str(self.max_participants)+", Ilmoittautuminen alkaa: "+str(self.signup_starts)+", Ilmoittautuminen loppuu: "+str(self.signup_ends)+", Yleiskuvaus: "+self.description

	def genInfo(self):
		if not self.prize:
			return "<li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: Ilmainen</li>"
		elif(self.prize==0):
			return "<li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: Ilmainen</li>"
		else:
			return "<p>Mikä-Missä-Milloin</p><p><ul><li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: "+str(self.prize)+"</li>"

	class Meta:
		abstract = True

class Sitz(CommonInfo):
	quotas=models.CharField(max_length=500,null=True, blank=True,verbose_name='Järjestävien tahojen osallistujakiintiöt')
#	avec=models.CharField(max_length=500,blank=True)
#	plaseerustoive=models.CharField(max_length=500,blank=True)
	def __str__(self):
		if self.quotas is None:
			return super().__str__()+", Osallistujakiintiöt: Ei ole"
		else:
			return super().__str__()+", Osallistujakiintiöt: "+self.quotas

class Annualfest(CommonInfo):
#	avec=models.CharField(max_length=500,blank=True)
#	plaseerustoive=models.CharField(max_length=500,blank=True)
	def __str__(self):
		return super().__str__()

class Excursion(CommonInfo):
	date=models.DateField(verbose_name='Ekskursion aloituspäivä')
	end_date=models.DateField(verbose_name='Ekskursion loppumispäivä')
	def __str__(self):
		return super().__str__()+", Päättymispäivä: "+str(self.end_date)

class OtherEvent(CommonInfo):
	min_participants=models.PositiveIntegerField(blank=True, null=True,verbose_name='Minimimäärä osallistujia')
	def __str__(self):
		return super().__str__()+", Minimimäärä osallistujia: "+str(self.min_participants)

class Participant(models.Model):
	event_type=models.ForeignKey(Events, on_delete=models.CASCADE,editable=False)
	name=models.CharField(max_length=200)
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
		return self.name+" ("+self.email+"), muut tiedot: "+self.miscInfo

class Archive(models.Model):
	event_type=models.CharField(max_length=500,verbose_name='Tapahtuman typpi')
	name=models.CharField(max_length=500,verbose_name='Tapahtuman nimi')
	description=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	participants=models.IntegerField(verbose_name='Osallistujamäärä')
	owner=models.CharField(max_length=500,verbose_name='Tapahtuman pitäjä')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	def __str__(self):
		return "Tapahtuman tyyppi: "+self.event_type+", Tapahtuman nimi: "+self.name+", Kokonaisosallistujamäärä: "+str(self.participants)+", Tapahtuman järjestäjä: "+self.owner+",Alkuperäinen pitopäivä: "+str(self.date)+", Yleiskuvaus: "+self.description
