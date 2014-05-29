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

menu_items = []

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
		self.add_menu_item("LIGHT", reverse("light"))
		self.add_menu_item("WHOIS", reverse("whois"))
		self.add_menu_item("INDEX", reverse("index"))

class IndexView(PrivateView):
	template_name = "private_index.html"

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
			if data[v]:
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

		temp = api.command("temp", "get")

		self.set("names", j["users"])
		self.set("temp", temp)

class LightView(PrivateView):
	template_name = "light.html"

	def __init__(self):
		super(LightView, self).__init__()

		data = api.command("light", "get_state", "all")
		for v in ["hardroom", "softroom", "corridor", "kitchen"]:
			if data[v]:
				self.set(v, "checked")
			else:
				self.set(v, "")

def temp(request):
	temp = api.command("temp", "get")
	return HttpResponse(temp)
