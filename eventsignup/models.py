from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

User = get_user_model()


# Kaikki uniikit tapahtumatyypit (esim. sitsit).
class EventType(models.Model):
    event_type = models.CharField(max_length=191, unique=True, verbose_name='Tapahtuman tyyppi')

    def __str__(self):
        return "Tapahtuman tyyppi: "+str(self.event_type)


# Tapahtuman järjestäjä (esim. Asteriski).
#class EventOwner(models.Model):
#    name = models.CharField(max_length=191, unique=True, verbose_name='Järjestävä taho')
#    email = models.EmailField(verbose_name='Sähköpostiosoite')
#
#    def __str__(self):
#        return "Tapahtuman järjestäjä(t): "+str(self.name)+", Sähköposti: "+str(self.email)


# Kaikki tapahtumat koodusti.
class Events(models.Model):
    event_type = models.ForeignKey(EventType, to_field='event_type', on_delete=models.CASCADE)
    uid = models.PositiveIntegerField(primary_key=True)
    #    owner=models.ForeignKey(EventOwner, to_field='name', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event_type)+", uid: "+str(self.uid)+", tapahtuman järjestäjä(t) : "+str(self.owner)


# Eri tapahtumatyyppien yhteiset attribuutit.
# Abstrakti yläluokka.
class CommonInfo(models.Model):
    # kaikki yhteiset attribuutit tähän
    uid = models.ForeignKey(Events, on_delete=models.CASCADE, editable=False)
    event_type = models.ForeignKey(EventType, to_field='event_type', on_delete=models.CASCADE, editable=False)
    #    owner=models.ForeignKey(EventOwner, to_field='name', on_delete=models.CASCADE,editable=False)
    owner = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=200, verbose_name='Tapahtuman nimi')
    place = models.CharField(max_length=200, verbose_name='Pitopaikka')
    date = models.DateField(verbose_name='Tapahtuman pitopäivä')
    start_time = models.TimeField(verbose_name='Tapahtuman alkamisaika', default='00:00:00')
    description = models.TextField(verbose_name='Tapahtuman yleiskuvaus')
    pic = models.ImageField(blank=True, null=True, verbose_name='Ilmoittautumislomakkeen kansikuva', upload_to='events/%Y/%m/')
    prize = models.CharField(max_length=200, blank=True, null=True, verbose_name='Tapahtuman hinta')
    max_participants = models.PositiveIntegerField(blank=True, null=True, verbose_name='Maksimimäärä osallistujia')
    signup_starts = models.DateTimeField(verbose_name='Tapahtumaan ilmoittautuminen avautuu')
    signup_ends = models.DateTimeField(blank=True, null=True, verbose_name='Tapahtumaan ilmoittautuminen sulkeutuu')
    has_reserve_spots = models.BooleanField(verbose_name='Ota ilmoittautumisen varasijat käyttöön')

    def save(self, *args, **kwargs):
        self.description = mark_safe(self.description.replace("\n", "<br/>"))
        super(CommonInfo, self).save(*args, **kwargs)

    def __str__(self):
        return "Tapahtuman järjestäjä: "+str(self.owner)+", Tapahtuman tyyppi: "+str(self.event_type)+", Tapahtuman nimi: "+self.name+", Pitopaikka "+self.place+", Hinta: "+str(self.prize)+", Tapahtuman pitopäivä: "+str(self.date)+", Maksimi osallistujamäärä: "+str(self.max_participants)+", Ilmoittautuminen alkaa: "+str(self.signup_starts)+", Ilmoittautuminen loppuu: "+str(self.signup_ends)+", Yleiskuvaus: "+self.description

    def gen_info(self):
        if not self.prize:
            return "<li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: Ilmainen</li>"
        elif self.prize==0:
            return "<li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: Ilmainen</li>"
        else:
            return "<p>Mikä-Missä-Milloin</p><p><ul><li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: "+str(self.prize)+"</li>"

    class Meta:
        abstract = True


# Sitsit tyyppinen tapahtuma.
class Sitz(CommonInfo):
    quotas = models.CharField(max_length=191, null=True, blank=True, verbose_name='Järjestävien tahojen osallistujakiintiöt')

    def __str__(self):
        if self.quotas is None:
            return super().__str__()+", Osallistujakiintiöt: Ei ole"
        else:
            return super().__str__()+", Osallistujakiintiöt: "+self.quotas


# Vuosijuhlat tyyppinen tapahtuman.
class Annualfest(CommonInfo):
    def __str__(self):
        return super().__str__()


# Ekskurisio tyyppinen tapahtuma.
class Excursion(CommonInfo):
    date = models.DateField(verbose_name='Ekskursion aloituspäivä')
    end_date = models.DateField(verbose_name='Ekskursion loppumispäivä')

    def __str__(self):
        return super().__str__()+", Päättymispäivä: "+str(self.end_date)


# Muu ennalta määrittelemätön tapahtuma.
class OtherEvent(CommonInfo):
    min_participants = models.PositiveIntegerField(blank=True, null=True, verbose_name='Minimimäärä osallistujia')

    def __str__(self):
        return super().__str__()+", Minimimäärä osallistujia: "+str(self.min_participants)


# Tapahtumaan osallistuja.
class Participant(models.Model):
    event_type = models.ForeignKey(Events, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=200, verbose_name='Nimi')
    email = models.EmailField(verbose_name='Sähköpostiosoite')
    vege = models.NullBooleanField(blank=True, null=True)
    nonholic = models.NullBooleanField(blank=True, null=True)
    avec = models.CharField(max_length=100, blank=True, null=True)
    plaseeraus = models.CharField(max_length=500, blank=True, null=True)
    quota = models.CharField(max_length=200, blank=True, null=True, editable=False)
    reserve_spot = models.BooleanField(editable=False)
    gender = models.CharField(max_length=10, blank=True, null=True)
    #    Tämä kenttä sisältää tiedot: jäsen/ei jäsen, onko maksanut.
    #    datan tulee olla muodossa {member:arvo, hasPaid:arvo}
    # miscInfo = models.TextField(editable=False)
    member = models.NullBooleanField(editable=False, blank=True, null=True)
    hasPaid = models.NullBooleanField(editable=False, blank=True, null=True)

    def __str__(self):
        return str(self.event_type)+', ' + self.name+" ("+self.email+"), vege: "+str(self.vege)+", holiton: "+str(self.nonholic)+', avec: '+str(self.avec)+', plaseeraus: '+str(self.plaseeraus)+', quota: '+str(self.quota)+', jäsen: '+str(self.member)+', maksanut: '+str(self.hasPaid)


# Arkistotaulu.
class Archive(models.Model):
    event_type = models.CharField(max_length=191, verbose_name='Tapahtuman typpi')
    name = models.CharField(max_length=191, verbose_name='Tapahtuman nimi')
    description = models.TextField(verbose_name='Tapahtuman yleiskuvaus')
    participants = models.IntegerField(verbose_name='Osallistujamäärä')
    owner = models.CharField(max_length=191, verbose_name='Tapahtuman pitäjä')
    date = models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
    place = models.CharField(max_length=191, verbose_name='Pitopaikka')
    pic = models.ImageField(blank=True, null=True, verbose_name='Ilmoittautumislomakkeen kansikuva')
    prize = models.CharField(max_length=191, blank=True, null=True, verbose_name='Tapahtuman hinta')

    def __str__(self):
        return "Tapahtuman tyyppi: "+self.event_type+", Tapahtuman nimi: "+self.name+", Kokonaisosallistujamäärä: "+str(self.participants)+", Tapahtuman järjestäjä: "+self.owner+",Alkuperäinen pitopäivä: "+str(self.date)+", Yleiskuvaus: "+self.description+', Alkuperäinen pitopaikka: '+self.place+', Mitä maksoi: '+self.prize
