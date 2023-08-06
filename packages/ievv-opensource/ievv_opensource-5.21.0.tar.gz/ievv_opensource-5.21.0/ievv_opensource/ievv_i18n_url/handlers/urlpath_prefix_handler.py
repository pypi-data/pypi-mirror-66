import posixpath
import urllib.parse

from . import abstract_handler


class UrlpathPrefixHandler(abstract_handler.AbstractHandler):
    """
    I18n url handler that matches languages based on a URL prefix.
    """

    #: URL path prefix before we look for the languagecode in the url.
    #: **Must not** start or end with ``/``.
    #:
    #: E.g.:
    #:
    #: - If your languages should be served at ``/<languagecode>``, this should be blank string.
    #: - If your languages should be served at ``/my/translations/<languagecode>``, this should be ``my/translations``.
    LANGUAGECODE_URLPATH_PREFIX = ''

    @classmethod
    def get_urlpath_prefix_for_languagecode(cls, base_url, languagecode):
        if languagecode == cls.detect_default_languagecode(base_url):
            return ''
        if cls.LANGUAGECODE_URLPATH_PREFIX:
            return f'{cls.LANGUAGECODE_URLPATH_PREFIX}/{languagecode}'
        return languagecode

    def strip_languagecode_from_urlpath(self, path):
        if self.__class__.LANGUAGECODE_URLPATH_PREFIX:
            full_prefix = f'/{self.__class__.LANGUAGECODE_URLPATH_PREFIX}/'
            if not path.startswith(full_prefix):
                return path
            path_without_prefix = path[len(full_prefix):]
        else:
            path_without_prefix = path[1:]
        splitpath = path_without_prefix.split(posixpath.sep, 1)
        if not splitpath:
            return path
        languagecode = splitpath[0]
        if not self.is_supported_languagecode(languagecode):
            return path
        return f'/{splitpath[1]}'

    @classmethod
    def _detect_languagecode_from_urlpath(cls, path):
        if cls.LANGUAGECODE_URLPATH_PREFIX:
            full_prefix = f'/{cls.LANGUAGECODE_URLPATH_PREFIX}/'
            if not path.startswith(full_prefix):
                return None
            path_without_prefix = path[len(full_prefix):]
        else:
            path_without_prefix = path[1:]
        splitpath = path_without_prefix.split(posixpath.sep, 1)
        if not splitpath:
            return None
        return splitpath[0]

    def get_languagecode_from_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return self.__class__._detect_languagecode_from_urlpath(parsed_url.path)

    @classmethod
    def detect_current_languagecode(cls, base_url, request):
        return cls._detect_languagecode_from_urlpath(request.path)

    def build_urlpath(self, path, languagecode=None):
        real_languagecode = languagecode or self.active_languagecode
        prefix = self.__class__.get_urlpath_prefix_for_languagecode(
            base_url=self.active_base_url, languagecode=real_languagecode)
        if prefix:
            full_path = f'/{prefix}{path}'
        else:
            full_path = path
        return full_path

    def build_absolute_url(self, path, languagecode=None):
        return self.active_base_url.build_absolute_url(
            self.build_urlpath(path=path, languagecode=languagecode))
