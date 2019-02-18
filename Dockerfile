FROM python:3.6

RUN mkdir /riskiwww
WORKDIR /riskiwww
ADD . /riskiwww

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
#RUN python manage.py createsuperuser --username admin --email admin@localhost

RUN python bootstrap_helper.py
