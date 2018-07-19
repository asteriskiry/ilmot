from django.urls import path

from . import views
app_name='eventsignup'
urlpatterns = [
    # näytä tervetuloa ja ohjaa sisäänkirjautumiseen
    path('', views.index, name='index'),
    # hallintakonsoli
    path('management',views.management, name='management'),
    # uuden tapahtuman lisäyslomake & dropdown menu
    path('event/add/<str:type>', views.add,name='add'),
    path('event/add/', views.formtype,name='formtype'),
    # sivupaneelin "nippelitieto"
    path('event/<int:uid>/stats/', views.stats, name='stats'),
    # preview uuden tapahtuman luomisen jälkeen
    path('event/<int:uid>/preview/', views.preview, name='preview'),
     # tapahtuman info
    path('event/<int:uid>/view/', views.info, name='view'),
    # tapahtuman muokkaus
    path('event/<int:uid>/edit/',views.edit, name='edit'),
    # tapahtumaan osallistujan ilmoittautumislomake
    path('event/<int:uid>/signup/', views.signup, name='signup'),
    # Poistaa (=Arkistoi) tapahtuman
    path('event/<int:uid>/delete/', views.archive, name='archive'),

]
