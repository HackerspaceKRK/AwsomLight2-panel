from urllib.request import *
import json

API_URL = "http://al2.hskrk.pl/api/v2"

def command(category, command, *args):
	url = "{}/{}/{}/{}".format(API_URL, category, command, "/".join(list(args)))
	f = urlopen(url)
	cnt = f.read()
	return json.loads(cnt.decode())
