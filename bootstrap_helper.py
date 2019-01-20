#!/usr/bin/env python3
import os

# Luo tietokantaan muut vaaditut datat sekä
# luo superuserin sekä testikäyttäjän, jolla on oikeat oikeudet kantaan.
def setupDjango():
	global eventTypes, accounts
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riskiwww.settings")
	import django
	django.setup()
	from eventsignup.models import EventType
	for x in ['custom','muutapahtuma','ekskursio','vuosijuhlat','sitz','sitsit']:
		etype=EventType(event_type=x)
		etype.save()
	eventTypes=True
	from django.contrib.auth.models import User
	from eventsignup.models import EventOwner
	print('Luodaan uusi superuser. Käyttäjätunnus/salasana: admin')
	user = User.objects.create_superuser('admin', 'admin@localhost', 'admin')
	user.save()
	name='testuser'
	email='testuser@example.com'
	print('Luodaan uusi testikäyttäjä, joka voi luoda uusia tapahtumia. Käyttäjänimi/salasana on: testuser')
	user = User.objects.create_user(name, email, 'testuser')
	user.save()
	user=User.objects.get(username=name)
	print('Asetetaan testikäyttäjälle oikeat käyttöoikeudet.')
	from django.contrib.auth.models import Permission
#	perms=list(Permission.objects.values_list('codename',flat=True))
	for x in list(Permission.objects.values_list('codename',flat=True)):
		if(not ('log' in x or 'group' in x or 'permission' in x or 'user' in x or 'type' in x or 'owner' in x or 'session' in x)):
#			permission=Permission.objects.get(codename=x)
			user.user_permissions.add(Permission.objects.get(codename=x))
	user.save()
	eowner=EventOwner(email=email,name=name)
	eowner.save()
	accounts=True

# Lataa ja purkaa Bulma css:n tiedostot oikeaan paikkaan.
def setupBulma():
	global bulma
	import urllib.request
	import shutil, zipfile
	with urllib.request.urlopen('https://github.com/jgthms/bulma/releases/download/0.7.2/bulma-0.7.2.zip') as response, open('delete_me.zip', 'wb') as out_file:
	    shutil.copyfileobj(response, out_file)
	with zipfile.ZipFile('./delete_me.zip', 'r') as zipref:
		zipref.extractall('./mybulma/')
	os.unlink('./delete_me.zip')
	shutil.rmtree('./mybulma/__MACOSX/')
	bulma=True

def printResults():
	if eventTypes:
		print('EventTypes luotiin tietokantaan onnistuneesti.')
	else:
		print('EventTypes luominen epäonnistui.')
	if accounts:
		print('Uusi käyttäjä luotiin onnistuneesti.')
	else:
		print('Uuden käyttäjän luominen epäonnistui.')
	if bulma:
		print('Bulma paketin purku onnistui.')
	else:
		print('Bulma paketin purku epäonnistui')


eventTypes=False
accounts=False
bulma=False
setupDjango()
setupBulma()
printResults()

