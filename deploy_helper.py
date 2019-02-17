#!/usr/bin/env python3
import os
import sys
import urllib.request
import shutil
import zipfile


# Luo tietokantaan muut vaaditut datat sekä
# luo superuserin sekä käyttäjän, jolla on oikeat oikeudet kantaan.
def setupDjango():
    global eventTypes, accounts
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riskiwww.settings")
    import django
    django.setup()
    from eventsignup.models import EventType
    for x in ['custom', 'muutapahtuma', 'ekskursio', 'vuosijuhlat', 'sitz', 'sitsit']:
        etype=EventType(event_type=x)
        etype.save()
    eventTypes = True
    from django.contrib.auth.models import User
#    from eventsignup.models import EventOwner
    print('Luodaan uusi superuser.')
    uname = input('Anna haluttu käyttäjänimi: ')
    pw = input('Anna salasana: ')
    user = User.objects.create_superuser(uname, 'www-asteriski@utu.fi', pw)
    user.save()
    print('Luodaan uusi käyttäjä, joka voi luoda uusia tapahtumia. Käyttäjätunnus: asteriski')
    name = 'asteriski'
    pw = input('Anna salasana: ')
    user = User.objects.create_user(name, 'asteriski@utu.fi', pw)
    user.save()
    user = User.objects.get(username=name)
    print('Asetetaan käyttäjälle <'+name+'> oikeat käyttöoikeudet.')
    from django.contrib.auth.models import Permission
#    perms=list(Permission.objects.values_list('codename',flat=True))
    for x in list(Permission.objects.values_list('codename', flat=True)):
        if(not ('log' in x or 'group' in x or 'permission' in x or 'user' in x or 'type' in x or 'owner' in x or 'session' in x)):
#            permission=Permission.objects.get(codename=x)
            user.user_permissions.add(Permission.objects.get(codename=x))
    user.save()


# Lataa ja purkaa Bulma css:n tiedostot oikeaan paikkaan.
def setupBulma():
    global bulma
    print('Asennetaan Bulma css.')
    with urllib.request.urlopen('https://github.com/jgthms/bulma/releases/download/0.7.2/bulma-0.7.2.zip') as response, open('delete_me.zip', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile('./delete_me.zip', 'r') as zipref:
        zipref.extractall('./mybulma/')
    os.unlink('./delete_me.zip')
    shutil.rmtree('./mybulma/__MACOSX/')


def setupEnv():
    from django.core.management.utils import get_random_secret_key
    print('Luodaa tarvittava .env tiedosto.')
    with open('./riskiwww/.env', 'w') as f:
        f.write('SECRET_KEY='+get_random_secret_key())
        f.write('DEBUG=False')
        f.write('ALLOWED_HOSTS=.localhost,127.0.0.1,ilmot.asteriski.fi')
        db_name = input('Anna tietokannan nimi: ')
        db_user = input('Anna tietokantaan tarvittava käyttäjätunnus: ')
        db_pw = input('Anna salasana: ')
        db_host = input('Anna tietokantapalvelimen ip osoite: ')
        db_port = input('Anna käytetty portti: ')
        f.write("DATABASE_URL={'ENGINE': 'django.db.backends.mysql','NAME': '"+db_name+"','USER': '"+db_user+"','PASSWORD': '"+db_pw+"',    'HOST': '"+db_host+"','PORT': '"+db_port+"',}}")
        f.write('EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend')
        email_host = input('Anna smtp palvelimen nimi: ')
        f.write('EMAIL_HOST='+email_host)
        email_user = input('Anna smtp palvelimen käyttäjänimi (jos tarvitaan): ')
        email_pw = input('Anna salasana (jos tarvitaan): ')
        if(not (email_pw is None)):
            f.write('EMAIL_HOST_PASSWORD='+email_pw)
        if(not(email_user is None)):
            f.write('EMAIL_HOST_USER='+email_user)
        f.write('EMAIL_PORT=')
        f.write('SECURE_CONTENT_TYPE_NOSNIFF=True')
        f.write('SECURE_BROWSER_XSS_FILTER=True')
        f.write('SESSION_COOKIE_SECURE=True')
        f.write('CSRF_COOKIE_SECURE=True')
        f.write('X_FRAME_OPTIONS=DENY')
        f.write('SESSION_COOKIE_SECURE=True')


if __name__ == '__main__':
    setupEnv()
    setupDjango()
    setupBulma()
