from django.conf.urls import *

from public import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^whois$', views.WhoisView.as_view(), name='whois'),
	url(r'^temp$', views.temp),
)
