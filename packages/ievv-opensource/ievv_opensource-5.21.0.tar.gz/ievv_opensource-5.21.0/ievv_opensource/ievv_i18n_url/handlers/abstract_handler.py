import urllib.parse

from django.conf import settings
from django.utils.translation import get_language_info

from ievv_opensource.ievv_i18n_url import active_i18n_url_translation
from ievv_opensource.ievv_i18n_url.base_url import BaseUrl


class AbstractHandler:
    """
    Base class for `ievv_i18n_url` handlers.
    """
    def is_default_languagecode(self, languagecode):
        """Is the provided languagecode the default language code?

        Note that this may be per domain etc. depending on the handler class.

        Args:
            languagecode (str): Language code.

        Returns:
            bool: True if the provided languagecode is the default.
        """
        return languagecode == self.default_languagecode

    @property
    def default_languagecode(self):
        """Get the default language code.

        Note that this may be per domain etc. depending on the handler class.

        Defaults to ``settings.LANGUAGE_CODE``.

        Returns:
            str: Default languagecode.
        """
        return active_i18n_url_translation.get_default_languagecode()

    @property
    def active_languagecode(self):
        """Get the active languagecode.

        Returns:
            str: The active languagecode.
        """
        return active_i18n_url_translation.get_active_languagecode()

    @property
    def active_languagecode_or_none_if_default(self):
        """Get the active languagecode, but returns None if the active languagecode is
        the default languagecode.

        Returns:
            str: The active languagecode, or None if the active languagecode is the default languagecode.
        """
        languagecode = self.active_languagecode
        if self.is_default_languagecode(languagecode):
            return None
        return languagecode

    @property
    def active_base_url(self):
        """Get the active base url.

        Returns:
            str: The active base url.
        """
        return active_i18n_url_translation.get_active_base_url()

    @classmethod
    def is_supported_languagecode(cls, languagecode):
        """Is the provided languagecode a supported languagecode?

        Args:
            languagecode (str): Language code.

        Returns:
            bool: True if the provided languagecode is supported.
        """
        return languagecode in cls.get_supported_languagecodes()

    def get_translated_label_for_languagecode(self, languagecode):
        """Get the translated label for the languagecode (the name of the language)
        in the currently active language.

        This defaults to the english name for the language fetched
        via ``django.utils.translation.get_language_info()``.

        This is typically used in subclasses that override :meth:`~.AbstractHandler.get_label_for_languagecode`
        and change to translated labels by default.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Translated label for the languagecode.
        """
        language_info = get_language_info(languagecode)
        return language_info['name_translated']

    def get_untranslated_label_for_languagecode(self, languagecode):
        """Get the untranslated label for the languagecode (the name of the language).

        Should return a label for the languagecode in a commonly used
        language that most users of your site will understand.

        This defaults to the english name for the language fetched
        via ``django.utils.translation.get_language_info()``.

        This is the what the default implementation of :meth:`~.AbstractHandler.get_label_for_languagecode`
        uses.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Unstranslated label for the languagecode.
        """
        language_info = get_language_info(languagecode)
        return language_info['name']

    def get_local_label_for_languagecode(self, languagecode):
        """Get the local label for the languagecode (the name of the language in that language).

        This defaults to the english name for the language fetched
        via ``django.utils.translation.get_language_info()``.

        This is typically used in subclasses that override :meth:`~.AbstractHandler.get_label_for_languagecode`
        and change to labels in the native language by default.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Local label for the languagecode.
        """
        language_info = get_language_info(languagecode)
        return language_info['name_local']

    def get_label_for_languagecode(self, languagecode):
        """Get the label for the languagecode (the name of the language).

        Defaults to using :meth:`~.AbstractHandler.get_local_label_for_languagecode`.
        I.e.: We use the native/local translation of the language name as
        language label by default.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Label for the languagecode.
        """
        return self.get_local_label_for_languagecode(languagecode)

    @classmethod
    def build_base_url_from_request(cls, request):
        return BaseUrl(request.build_absolute_uri('/'))

    @classmethod
    def _detect_activate_translation_kwargs_from_request(cls, request):
        active_base_url = cls.build_base_url_from_request(request=request)
        default_languagecode = cls.detect_default_languagecode(base_url=active_base_url)
        if cls.is_translatable_urlpath(active_base_url, request.path):
            current_languagecode = cls.detect_current_languagecode(base_url=active_base_url, request=request)
            if not current_languagecode or not cls.is_supported_languagecode(current_languagecode):
                current_languagecode = default_languagecode
        else:
            current_languagecode = default_languagecode
        active_language_urlpath_prefix = cls.get_urlpath_prefix_for_languagecode(
            base_url=active_base_url,
            languagecode=current_languagecode)
        return {
            'active_translation_languagecode': cls.get_translation_to_activate_for_languagecode(current_languagecode),
            'active_languagecode': current_languagecode,
            'default_languagecode': default_languagecode,
            'active_language_urlpath_prefix': active_language_urlpath_prefix,
            'active_base_url': active_base_url
        }

    @classmethod
    def activate_languagecode_from_request(cls, request):
        """Activate the detected languagecode.

        This is what :class:`ievv_opensource.ievv_i18n_url.middleware.LocaleMiddleware`
        uses to process the request.

        What this does:

        - Builds a base_url using ``request.build_absolute_uri('/')``.
        - Finds the default language code using :meth:`~.AbstractHandler.detect_default_languagecode`
        - Finds the current language code using :meth:`~.AbstractHandler.detect_current_languagecode`
        - Handles fallback to default languagecode if the current languagecode is unsupported or the requested
          url path is not not translatable (using :meth:`~.AbstractHandler.is_supported_languagecode`
          and :meth:`~.AbstractHandler.is_translatable_urlpath`).
        - Finds the language URL prefix :meth:`~.AbstractHandler.get_urlpath_prefix_for_languagecode`.
        - Activates the current language/translation using
          :func:`ievv_opensource.ievv_i18n_url.active_i18n_url_translation.activate`.

        .. warning::

            Do not override this method, and you should normally not call this method.
            I.e.: This is for the middleware.
        """
        active_i18n_url_translation.activate(**cls._detect_activate_translation_kwargs_from_request(request=request))

    ##################################################
    #
    # Methods designed to be overridden in subclasses:
    #
    ##################################################

    def get_icon_cssclass_for_languagecode(self, languagecode):
        """Get an icon CSS class for the language code.

        This is typically implemented on a per app basis. I.e.: The application
        creates a subclass of one of the built-in handlers and override this
        to provide icons for their supported languages. This is provided as
        part of the handler to make it possible to generalize things like
        rendering language selects with icons.

        This icon must be possible to use in HTML like this::

            <span class="ICON_CSS_CLASS_HERE"></span>

        Args:
            languagecode (str): Language code.

        Returns:
            str: Icon css class
        """
        return None

    def get_icon_svg_image_url_for_languagecode(self, languagecode):
        """Get an icon SVG image URL for the language code.

        This is typically implemented on a per app basis. I.e.: The application
        creates a subclass of one of the built-in handlers and override this
        to provide icons for their supported languages. This is provided as
        part of the handler to make it possible to generalize things like
        rendering language selects with icons.

        Args:
            languagecode (str): Language code.

        Returns:
            str: SVG image URL.
        """
        return None

    def build_absolute_url(self, path, languagecode=None):
        """Build absolute uri for the provided path within the provided languagecode.

        MUST be implemented in subclasses.

        .. note::

            Session based handlers will ignore the languagecode argument and just return
            the URL for the default translation. This is because all their translations live at the same URL.
            See the *A warning about session based translations* in the docs for more details.

        Args:
            path (str): The path (same format as HttpRequest.get_full_path()
                returns - e.g: ``"/my/path?option1&option2"``)
            languagecode (str, optional): The languagecode to build the URI for. Defaults to None, which
                means we build the URI within the current languagecode.
        """
        raise NotImplementedError()

    def build_urlpath(self, path, languagecode=None):
        """Build URL path for the provided path within the provided languagecode.

        This is a compatibility layer to make it possible to work with older code
        that considers a URL path as fully qualified. Most handlers will just
        do nothing with the path, or prepend a prefix, but some handlers (those that work with multiple domains),
        will use the ``ievv_i18n_url_redirect_to_languagecode`` redirect view here to
        return an URL that will redirect the user to the correct URL.

        MUST be implemented in subclasses.

        .. note::

            Session based handlers will ignore the languagecode argument and just return
            the PATH for the default translation. This is because all their translations live at the same URL.
            See the *A warning about session based translations* in the docs for more details.

        Args:
            path (str): The path (same format as HttpRequest.get_full_path()
                returns - e.g: ``"/my/path?option1&option2"``)
            languagecode (str, optional): The languagecode to build the path for. Defaults to None, which
                means we build the URI within the current languagecode.
        """
        raise NotImplementedError()

    def transform_url_to_languagecode(self, url, languagecode):
        """Transform the provided url into the "same" url, but in the provided languagecode.

        MUST be implemented in subclasses.

        .. note::

            This is not possible to implement in a safe
            manner for session based handlers (I.e.: multiple translation live at the same URI),
            so for these kind of handler this method will just return the provided `url`.
            See the *A warning about session based translations* in the docs for more details.

        Args:
            url (str): The URL to transform.
            languagecode (str): The languagecode to transform the URL into.
        """
        raise NotImplementedError()

    @classmethod
    def get_translation_to_activate_for_languagecode(cls, languagecode):
        """Get the languagecode to actually activate for the provided languagecode.

        Used by the middleware provided by `ievv_i18n_url` to activate the translation for the
        provided languagecode.

        This is here to make it possible for applications to have languages that has their
        own domains or URLs, but show translations from another language code. E.g.:
        you may have content in a language, but be OK with translation strings from another language.

        Returns:
            str: The languagecode to activate with the django translation system for the provided ``languagecode``.
            Defaults to the provided ``languagecode``.
        """
        return languagecode

    @classmethod
    def get_supported_languagecodes(cls):
        """Get supported language codes.

        Defaults to the language codes in ``settings.LANGUAGES``.

        Returns:
            set: A set of the supported language codes.
        """
        return {l[0] for l in settings.LANGUAGES}

    def strip_languagecode_from_urlpath(self, path):
        raise NotImplementedError()

    def get_languagecode_from_url(self, url):
        raise NotImplementedError()

    @classmethod
    def is_translatable_urlpath(self, base_url, path):
        """Is the provided URL path translatable within the current base_url?

        We default to consider the paths in settings.MEDIA_URL and settings.STATIC_URL as untranslatable.

        If this returns ``False``, the middleware will use the default translation when serving
        the path.

        If you subclass this, you should not write code that parses the querystring part of the
        path. This will not work as intended (will not work the same everywhere) since the middleware
        does not call this with the querystring included, but other code using this may pass in the path
        with the querystring.

        Args:
            base_url (ievv_opensource.ievv_i18n_url.base_url.BaseUrl):
                The base URL - see :class:`ievv_opensource.ievv_i18n_url.base_url.BaseUrl` for more info.
            path (str): An URL path (e.g: ``/my/path``, ``/my/path?a=1&b=2``, etc.)
        Returns:
            bool: Is the provided URL translatable?
        """
        if settings.STATIC_URL and path.startswith(settings.STATIC_URL):
            return False
        if settings.MEDIA_URL and path.startswith(settings.MEDIA_URL):
            return False
        return True

    @classmethod
    def detect_preferred_languagecode_for_user(cls, user):
        """Detect the preferred languagecode for the provided user.

        This is normally NOT used by :meth:`~.AbstractHandler.detect_current_languagecode`
        except for handlers like the session handler where the URL does not change based
        on language code. E.g.: It would be strange to serve a language based on user
        preferences when the URL explicitly says what language code we are serving.

        This is mostly a convenience for management scripts, and a utility if you want to
        redirect users based on the preferred language code.

        Args:
            user: A user model object.

        Returns:
            str: The preferred language code for the provided user, or None.
            None means that the user has no preferred language code,
            or that the handler does not respect user preferences. Returns ``None`` by default.
        """
        return None

    @classmethod
    def detect_current_languagecode(cls, base_url, request):
        """Detect the current languagecode from the provided request and/or base_url.

        Used by the middleware provided by `ievv_i18n_url` find the current language code
        and set it on the current request.

        DO NOT USE THIS - it is for the middleware. Use :obj:`~.AbstractHandler.current_languagecode`.

        MUST be overridden in subclasses.

        If this returns None, it means that we should use the default languagecode. I.e.: Do not handle
        fallback to default languagecode when implementing this method in subclasses - just return None.

        Args:
            base_url (ievv_opensource.ievv_i18n_url.base_url.BaseUrl):
                The base URL - see :class:`ievv_opensource.ievv_i18n_url.base_url.BaseUrl` for more info.
            request (django.http.HttpRequest): The HttpRequest

        Returns:
            str: The current languagecode or None (None means default languagecode is detected).
        """
        raise NotImplementedError()

    @classmethod
    def detect_default_languagecode(cls, base_url):
        """Detect the default languagecode for the provided base_url.

        This is here so that handlers can override it to support different default languagecode
        per domain or perhaps more fancy stuff based on the provided url.

        Args:
            base_url (django.http.HttpRequest):
                The base URL - e.g: https://example.com, http://www.example.com:8080, ...
                (NOT https://example.com/my/path, https://example.com/en, ...).

        Returns:
            str: The default languagecode. Defaults to ``settings.LANGUAGE_CODE``.
        """
        return settings.LANGUAGE_CODE

    @classmethod
    def get_urlpath_prefix_for_languagecode(cls, base_url, languagecode):
        """
        Get the URL path prefix for the provided languagecode within the current base_url.

        Args:
            base_url (ievv_opensource.ievv_i18n_url.base_url.BaseUrl):
                The base URL - see :class:`ievv_opensource.ievv_i18n_url.base_url.BaseUrl` for more info.
            languagecode (str): The language code to find the prefix for.

        Returns:
            str: The url path prefix. **Can not** start or end with ``/``.
        """
        return ''
