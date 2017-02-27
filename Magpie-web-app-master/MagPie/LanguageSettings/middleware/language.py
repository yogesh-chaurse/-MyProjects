__author__ = 'webonise'

from django.utils import translation
from django.conf import settings

class LanguageSettings(object):
    def process_request(self, request):
        if 'language_code' in request.session:
            translation.activate(request.session['language_code'])
        else:
            translation.activate(settings.LANGUAGE_CODE)
        return None

    def process_response(self, request, response):
        if 'language_code' in request.session:
            translation.activate(request.session['language_code'])
        else:
            translation.activate(settings.LANGUAGE_CODE)
        return response
