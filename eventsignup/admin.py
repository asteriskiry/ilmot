from django.contrib import admin

# Register your models here.
from .models import Sitz, Annualfest, OtherEvent, Excursion, Participant, EventType, Events, Archive

admin.site.register(Sitz)
admin.site.register(Annualfest)
admin.site.register(OtherEvent)
admin.site.register(Excursion)
admin.site.register(Participant)
admin.site.register(EventType)
#admin.site.register(EventOwner)
admin.site.register(Events)
admin.site.register(Archive)
