# ilmojärjestelmä
Asteriskin tapahtumailmoittautumisjärjestelmä

Ohjeet devauksen aloittamiseen:

1. Asenna Docker, Windows ja Mac: https://www.docker.com/products/docker-desktop tai Linux: https://docs.docker.com/install/linux/docker-ce/ubuntu/
2. Kloonaa asteriskiry/ilmot
3. Aja projektin juurikansiossa komento:  docker-compose up

Mikäli käytät Linuxia tee vielä tämä:

1. Laita Docker Daemon kuuntelemaan myös tcp porttia unix socketin lisäksi (sockettia voi käyttää vain roottina): https://docs.docker.com/install/linux/linux-postinstall/#configure-where-the-docker-daemon-listens-for-connections
2. käytä käynnistykseen tätä komentoa yllä olevan sijaan: docker-compose -H 127.0.0.1:portti up (jossa portti on se portti, jonka valitsit edellisessä kohdassa).
