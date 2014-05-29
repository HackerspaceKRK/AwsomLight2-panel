from django.shortcuts import *
from django.core import *
from django.conf import settings
from django.core.urlresolvers import *
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.views.generic import *
from DefaultView import *
import time, re, json
from urllib.request import *
import api

class PublicView(DefaultView):

	def __init__(self):
		super(PublicView, self).__init__()
		self.add_menu_item("WHOIS", reverse("whois"))
		self.add_menu_item("INDEX", reverse("index"))

class IndexView(PublicView):
	template_name = "public_index.html"

	def __init__(self):
		super(IndexView, self).__init__()

		cnt = urlopen(settings.WHOIS_URL).read()
		j = json.loads(cnt.decode())

		cnt = len(j["users"])
		self.set("users", cnt)

		rem = cnt % 10;
		osob_str = 'osób';
		znaj_str = 'znajduje';
		if cnt == 1: osob_str = 'osoba'
		elif (cnt < 10 or cnt > 20) and rem >= 2 and rem <= 4:
			osob_str = 'osoby'
			znaj_str = 'znajdują'
		self.set("osob_str", osob_str)
		self.set("znaj_str", znaj_str)
		self.set("names", ", ".join(j["users"]))

		data = api.command("light", "get_state", "all")
		for v in ["hardroom", "softroom", "corridor", "kitchen"]:
			self.set(v, "on" if data[v] else "off")

class WhoisView(PublicView):
	template_name = "whois.html"

	def __init__(self):
		super(WhoisView, self).__init__()

		cnt = urlopen(settings.WHOIS_URL).read()
		j = json.loads(cnt.decode())

		self.set("devices", j["total_devices_count"])

		temp = api.command("temp", "get")

		self.set("names", j["users"])
		self.set("temp", temp)

def temp(request):
	temp = api.command("temp", "get")
	return HttpResponse(temp)
