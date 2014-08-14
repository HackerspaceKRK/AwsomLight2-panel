from django.conf import settings
from django.utils.cache import patch_vary_headers

class MultiHostMiddleware:

	def process_request(self, request):
		try:
			ip = request.META["HTTP_X_FORWARDED_FOR"]
			if ip.startswith("10.12"):
				request.urlconf = "private.urls"
			else:
				request.urlconf = "public.urls"
			# host = request.META["HTTP_HOST"]
			# if ":" in host:
				# host = host.split(":")[0]
			# print(request.get_host())
			# request.urlconf = settings.HOST_MIDDLEWARE_URLCONF_MAP[host]
		except KeyError:
			pass # use default urlconf (settings.ROOT_URLCONF)

		def process_response(self, request, response):
			if getattr(request, "urlconf", None):
				patch_vary_headers(response, ('Host',))
				return response
