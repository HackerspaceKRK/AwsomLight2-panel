from django.shortcuts import *
from django.core import *
from django.core.urlresolvers import *
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
import time, re

def api(request):
	# temp = loader.get_template('index.html')
	# # a = LoginForm()

	# f = open("/home/krystiand/b", "rb")
	# txt = f.read().split("\n")[-2]
	# f.close()
	
	# # s = ""
	# # for line in txt:
		# # if "[temp]" in line:
			# # s = line

	# # m = re.search("\[temp\] read (\d+) fraq: (\d+).*", s)
	# # if m is not None:
		# # s = int(m.group(1)) + float(m.group(2)) / 16

	ctx = RequestContext(request, {})
	return HttpResponse("ASD")

