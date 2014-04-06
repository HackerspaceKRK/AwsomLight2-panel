from django.shortcuts import *
from django.core import *
from django.core.urlresolvers import *
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
import time, re
from django.views.generic import *

class DefaultView(TemplateView):
	menu_items = None
	values = None

	def __init__(self):
		super(DefaultView, self).__init__()
		self.menu_items = []
		self.values = {}
		
	def add_menu_item(self, name, url):
		self.menu_items.append({ "url": url, "name": name })

	def set(self, name, val):
		self.values[name] = val

	def get_context_data(self, **kwargs):
		menu = loader.get_template("menu.html")
		c = Context({ "menu_items": self.menu_items })
		context = super(TemplateView, self).get_context_data(**kwargs)
		context["menu"] = menu.render(c)
		for k, v in self.values.items():
			context[k] = v
		return context
