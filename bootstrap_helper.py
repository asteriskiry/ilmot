#!/usr/bin/env python3
import os
import sys
import urllib.request
import shutil
import zipfile


# Luo tietokantaan muut vaaditut datat sekä
# luo superuserin sekä testikäyttäjän, jolla on oikeat oikeudet kantaan.
def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riskiwww.settings")
    import django
    django.setup()
    from eventsignup.models import EventType
    for x in ['custom', 'muutapahtuma', 'ekskursio', 'vuosijuhlat', 'sitz', 'sitsit']:
        etype = EventType(event_type=x)
        etype.save()
    from django.contrib.auth.models import User
    print('Luodaan uusi superuser. Käyttäjätunnus/salasana: admin')
    user = User.objects.create_superuser('admin', 'admin@localhost', 'admin')
    user.save()
    print('Luodaan uusi testikäyttäjä, joka voi luoda uusia tapahtumia. Käyttäjänimi/salasana on: testuser')
    user = User.objects.create_user('testuser', 'testuser@example.com', 'testuser')
    user.save()
    user = User.objects.get(username='testuser')
    print('Asetetaan testikäyttäjälle oikeat käyttöoikeudet.')
    from django.contrib.auth.models import Permission
    for x in list(Permission.objects.values_list('codename', flat=True)):
        if not ('log' in x or 'group' in x or 'permission' in x or 'user' in x or 'type' in x or 'owner' in x or 'session' in x):
            user.user_permissions.add(Permission.objects.get(codename=x))
    user.save()


# Lataa ja purkaa Bulma css:n tiedostot oikeaan paikkaan.
def setup_bulma():
    print('Asennetaan Bulma css.')
    with urllib.request.urlopen('https://github.com/jgthms/bulma/releases/download/0.7.2/bulma-0.7.2.zip') as response, open('delete_me.zip', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile('./delete_me.zip', 'r') as zipref:
        zipref.extractall('/riskiwww/mybulma/')
    os.unlink('./delete_me.zip')
    shutil.rmtree('/riskiwww/mybulma/__MACOSX/')


# Kääntää css:n valmiiksi käytettävään muotoon.
def setup_css():
    global path
    print('Käännetään css.')
    import sass
    sass.compile(dirname=(path+"mybulma/sass/", path+"static/css/"))


def setup_env():
    print("Asetetaan muu dev ympäristö kuntoon.")
    print("Linkitetään oikea docker tiedosto dec ympäristöä varten.")
    os.link('./Dockerfile.dev', 'Dockerfile')
    os.link('./docker-compose.yml.dev', 'docker-compose.yml')


if __name__ == '__main__':
    path = os.path.abspath(__file__).replace(sys.argv[0], '')
    setup_django()
    setup_bulma()
    setup_css()
    setup_env()
    print('Valmis.')

