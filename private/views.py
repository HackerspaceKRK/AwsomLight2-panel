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
import kdhome

menu_items = []

lights = kdhome.KDHome()
lights.connect("localhost", 9999)

def add_menu_item(name, url):
	global menu_items
	menu_items.append({ "url": url, "name": name })

def go(request, template, d):
	ctx = RequestContext(request, d)
	menu = loader.get_template("menu.html")
	site = loader.select_template(["private_" + template + ".html", template + ".html"])

	c = Context({ "menu_items": menu_items })
	ctx["menu"] = menu.render(c)
	return HttpResponse(site.render(ctx))

class PrivateView(DefaultView):

	def __init__(self):
		super(PrivateView, self).__init__()
		#self.add_menu_item("LIGHT", reverse("light"))
		self.add_menu_item("WHOIS", reverse("whois"))
		self.add_menu_item("INDEX", reverse("index"))

class IndexView(PrivateView):
	template_name = "private_index.html"

	def __init__(self):
		super(IndexView, self).__init__()

		try:
			cnt = urlopen(settings.WHOIS_URL).read()
			j = json.loads(cnt.decode())
		except:
			j = { "users": [] }


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
		
		
		for v in ["HARDROOM", "SOFTROOM", "CORRIDOR", "KITCHEN", "CHILLROOM"]:
			state = lights.getOutput(v);
			if state == 0:
				self.set(v, "on")
			else:
				self.set(v, "off")

class WhoisView(PrivateView):
	template_name = "whois.html"

	def __init__(self):
		super(WhoisView, self).__init__()

		cnt = urlopen(settings.WHOIS_URL).read()
		j = json.loads(cnt.decode())

		self.set("devices", j["total_devices_count"])

		temp=666

		self.set("names", j["users"])
		self.set("temp", temp)

class LightView(PrivateView):
	template_name = "light.html"

	def __init__(self):
		super(LightView, self).__init__()

		for v in ["HARDROOM", "SOFTROOM", "CORRIDOR", "KITCHEN"]:
			state = lights.getOutput(v);
			if state == 0:
				self.set(v, "checked")
			else:
				self.set(v, "")


def temp(request):
	temp = 666
	return HttpResponse(temp)
