from django.conf.urls import *

from private import views
from private import api

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^whois', views.WhoisView.as_view(), name='whois'),
	url(r'^light', views.LightView.as_view(), name='light'),
	url(r'^temp', views.temp),
)
