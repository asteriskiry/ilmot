#!/usr/bin/env python3
import os
import sys
import urllib.request
import shutil
import zipfile
import subprocess


# Valmistelee tietokannan Djangon omalla migraatio työkalulla ja
# lisää tietokantaan muut vaaditut datat sekä
# luo superuserin sekä käyttäjän, jolla on oikeat oikeudet kantaan.
def setup_django():
    print('Laitetaan Django käyttökuntoon.\n')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riskiwww.settings")
    subprocess.run([pbin, "manage.py", "makemigrations"])
    subprocess.run([pbin, "manage.py", "migrate"])
    subprocess.run([pbin, "manage.py", "collectstatic"])
    import django
    django.setup()
    print('Lisätään kaikki EventTypes tietokantaan.\n')
    from eventsignup.models import EventType
    for x in ['custom', 'muutapahtuma', 'ekskursio', 'vuosijuhlat', 'sitz', 'sitsit']:
        etype = EventType(event_type=x)
        etype.save()
    from django.contrib.auth.models import User
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
    print('Asetetaan käyttäjälle <' + name + '> oikeat käyttöoikeudet.')
    from django.contrib.auth.models import Permission
    for x in list(Permission.objects.values_list('codename', flat=True)):
        if not (
                'log' in x or 'group' in x or 'permission' in x or 'user' in x or 'type' in x or 'owner' in x or 'session' in x):
            user.user_permissions.add(Permission.objects.get(codename=x))
    user.save()


# Lataa ja purkaa Bulma css:n tiedostot oikeaan paikkaan.
def setup_bulma():
    print('Ladataan ja puretaan Bulma css.\n')
    with urllib.request.urlopen(
            'https://github.com/jgthms/bulma/releases/download/0.7.2/bulma-0.7.2.zip') as response, open(
            'delete_me.zip', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile('./delete_me.zip', 'r') as zipref:
        zipref.extractall('./mybulma/')
    os.unlink('./delete_me.zip')
    shutil.rmtree('./mybulma/__MACOSX/')


def get_db_info():
    db_name = input('Anna tietokannan nimi: ')
    db_user = input('Anna tietokantaan tarvittava käyttäjätunnus: ')
    db_pw = input('Anna salasana: ')
    db_host = input('Anna tietokantapalvelimen ip osoite: ')
    # db_port = input('Anna käytetty portti: ')
    # return [db_name.replace('\n', ''), db_user.replace('\n', ''), db_pw.replace('\n', ''), db_host.replace('\n', ''), db_port.replace('\n', '')]
    return [db_name.replace('\n', ''), db_user.replace('\n', ''), db_pw.replace('\n', ''), db_host.replace('\n', '')]


def get_smtp_info():
    email_host = input('Anna smtp palvelimen nimi: ')
    email_user = input('Anna smtp palvelimen käyttäjänimi (jos tarvitaan): ')
    email_pw = input('Anna salasana (jos tarvitaan): ')
    # email_port = input('Anna smtp palvelimen käyttämä portti: ')
    # return [email_host.replace('\n', ''), email_user.replace('\n', ''), email_pw.replace('\n', ''), email_port.replace('\n', '')]
    return [email_host.replace('\n', ''), email_user.replace('\n', ''), email_pw.replace('\n', '')]


# Valmistelee järjestelmätason käyttöympäristön kuntoon ja
# generoi Djangolle tarvittavat konffit.
def setup_env(rerun):
    if not rerun:
        print('Asennetaan tarvittavat python moduulit.\n')
        try:
            with open(path + 'requirements.txt', 'r') as f:
                modules = []
                for line in f:
                    modules.append(line.replace('\n', ''))
                for module in modules:
                    subprocess.run(["pip3", "install", module])
        except IOError:
            print(
                'Tiedosto requirements.txt ei löydy! Skriptin suoritusta ei voi jatkaa. Varmista, että repo on kloonattu kunnolla.\n')
            exit(1)
    from django.core.management.utils import get_random_secret_key
    print('Luodaan tarvittava .env tiedosto.\n')
    forced_info = False
    if rerun:
        old_db_settings = ''
        old_smtp_settings = []
        old_url = ''
        try:
            with open(path + 'riskiwww/.env', 'r') as f:
                for line in f:
                    if 'DATABASE_URL' in line:
                        old_db_settings = line.replace('\n', '')
                    if 'EMAIL' in line:
                        old_smtp_settings.append(line.replace('\n', ''))
                    if 'ALLOWED_HOSTS' in line:
                        old_url = line.replace('\n', '')
        except IOError:
            print('Virhe! Vanhaa .env tiedostoa ei löydy. Asetusten uudelleen määrittely on pakollista.\n')
            forced_info = True
    with open(path + 'riskiwww/.env', 'w') as f:
        write_db = False
        write_smtp = False
        write_host = False
        url = ''
        f.write('SECRET_KEY=' + get_random_secret_key() + '\n')
        f.write('DEBUG=False\n')
        if forced_info or (rerun and input('Uusitaanko url tiedot? [k/e]: ').casefold() == 'k'):
            url = input(
                'Anna palvelimen domain nimi, josta palvelun saa kiinni (eg. url.asteriski.fi) (lisätään allowed host tietoihin): ')
            url = url.replace('\n', '')
            write_host = True
        elif not rerun:
            url = input(
                'Anna palvelimen domain nimi, josta palvelun saa kiinni (eg. url.asteriski.fi) (lisätään allowed host tietoihin): ')
            url = url.replace('\n', '')
            write_host = True
        if write_host:
            f.write('ALLOWED_HOSTS=.localhost,127.0.0.1,' + url + '\n')
        if forced_info or (rerun and input('Uusitaanko tietokannan tiedot? [k/e]: ').casefold() == 'k'):
            db_info = get_db_info()
            write_db = True
        elif not rerun:
            db_info = get_db_info()
            write_db = True
        if write_db:
            with open('./my.cnf', 'w') as e:
                e.write(
                    "# my.cnf\n[client]\ndatabase = " + db_info[0] + "\nuser = " + db_info[1] + "\npassword = " + db_info[
                        2] + "\ndefault-character-set = utf8\n")
            # f.write("DATABASE_URL='mysql://"+dbInfo[1]+":"+dbInfo[2]+"@"+dbInfo[3]+":3306/"+dbInfo[0]+"'\n")
        f.write("EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'\n")
        if forced_info or (rerun and input('Uusitaanko smtp asetukset? [k/e]: ').casefold() == 'k'):
            smtp_info = get_smtp_info()
            write_smtp = True
        elif not rerun:
            smtp_info = get_smtp_info()
            write_smtp = True
        if write_smtp:
            f.write('EMAIL_HOST=' + smtp_info[0] + '\n')
            if not (smtp_info[1] is None):
                f.write("EMAIL_HOST_PASSWORD='" + smtp_info[1] + "'\n")
            if not (smtp_info[2] is None):
                f.write("EMAIL_HOST_USER='" + smtp_info[2] + "'\n")
            f.write("EMAIL_PORT='25'\n")
        if rerun and not write_db:
            f.write(old_db_settings)
            f.write('\n')
        if rerun and not write_smtp:
            for line in old_smtp_settings:
                f.write(line + '\n')
        if rerun and not write_host:
            f.write(old_url + '\n')
        f.write('SECURE_CONTENT_TYPE_NOSNIFF=True\n')
        f.write('SECURE_BROWSER_XSS_FILTER=True\n')
        f.write('SESSION_COOKIE_SECURE=True\n')
        f.write('CSRF_COOKIE_SECURE=True\n')
        f.write("X_FRAME_OPTIONS='DENY'\n")
        f.write('SESSION_COOKIE_SECURE=True\n\n')
        f.write("STATIC_ROOT='" + path + "static/'\n")
    print('Generoidaan riskiwww_uwsgi.ini.')
    with open('riskiwww_uwsgi.ini', 'w')as f:
        f.write(
            "# riskiwww_uwsgi.ini file\n[uwsgi]\n\n# Django-related settings\n# the base directory (full path)\nchdir = " + path + "\n# Django's wsgi file\nmodule = riskiwww.wsgi\n# the virtualenv (full path)\n#home = /path/to/virtualenv\n\n# process-related settings\n# master\nmaster = true\n# maximum number of worker processes\nprocesses = 10\n# the socket (use the full path to be safe)\nsocket = /tmp/riskiwww.sock\n# ... with appropriate permissions - may be needed\n chmod-socket = 664\n# clear environment on exit\nvacuum = true\n")
    print("Linkitetään oikeat docker tiedostot prod ympäristöä varten.")
    os.link('./Dockerfile.prod', 'Dockerfile')
    os.link('./docker-compose.yml.prod', 'docker-compose.yml')


# Kääntää css:n valmiiksi käytettävään muotoon.
def setup_css():
    print('Käännetään css.')
    import sass
    sass.compile(dirname=(path + "mybulma/sass/", path + "static/css/"))


def print_env():
    print(
        'Konfiguraatiot luotiin seuraavilla tiedoilla. Mikäli syötetyissä tiedoissa oli virheitä, aja skripti uudestaan: ' + pbin + ' ' +
        sys.argv[0] + ' -r\n')
    with open(path + 'riskiwww/.env', 'r') as f:
        print('Djangon Konfiguraatiot .env')
        for line in f:
            print(line)
    with open(path + 'my.cnf', 'r') as e:
        print('\nTietokannan konfiguraatio my.cnf\n')
        for line in e:
            print(line)


pbin = sys.executable or 'python3'
path = os.path.abspath(__file__).replace(sys.argv[0], '')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-r':
            setup_env(True)
            print_env()
            exit()
        elif sys.argv[1] == '-s':
            setup_env(False)
            setup_django()
            setup_bulma()
            setup_css()
            print_env()
            exit()
        else:
            exit()
    else:
        print(
            'Jotta asennus onnistuu kunnolla, asenna järjestelmän paketinhallinnalla paketti, joka sisältää <mysql_config> tiedoston, mikäli sitä ei ole jo asennettu.\nVarmista myös, että käytettäväksi tarkoitettu tietokanta on olemassa ja käyttäjällä on tarvittavat lisää/poista/muokkaa yms oikeudet.\nAja sitten skripti uudestaan: ' + pbin + ' ' +
            sys.argv[0] + ' -s')
