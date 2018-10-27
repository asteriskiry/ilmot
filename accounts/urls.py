from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
app_name='accounts'
urlpatterns = [
	url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
    # login sivu
#    path('login/', views.login, name='login'),
#    ]
