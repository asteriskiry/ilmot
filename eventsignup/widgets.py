# source: https://djangosnippets.org/snippets/2027/
from django.forms.widgets import TextInput, DateInput, DateTimeInput, TimeInput


class MyEmailInput(TextInput):
    input_type = 'email'


class MyNumberInput(TextInput):
    input_type = 'number'


class MyTelephoneInput(TextInput):
    input_type = 'tel'


class MyDateInput(DateInput):
    input_type = 'date'


class MyDateTimeInput(DateTimeInput):
    input_type = 'datetime'


class MyTimeInput(TimeInput):
    input_type = 'time'

