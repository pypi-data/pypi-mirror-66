from django.utils import translation

from . import abstract_handler


class DjangoSessionHandler(abstract_handler.AbstractHandler):
    """
    Django session based i18n url handler.

    .. warning::

        Please read the *A warning about session based translations* in the docs before
        deciding to use this handler.
    """

    @classmethod
    def detect_current_languagecode(cls, base_url, request):
        return translation.get_language_from_request(request)

    def strip_languagecode_from_urlpath(self, path):
        return path

    def get_languagecode_from_url(self, url):
        return self.active_languagecode

    def build_absolute_url(self, path, languagecode=None):
        return self.active_base_url.build_absolute_url(path)

    def transform_url_to_languagecode(self, url, languagecode):
        return url
