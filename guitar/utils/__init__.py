from urllib.parse import quote, urljoin

from django.apps import apps
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.translation import string_concat


def get_random_url_password(length=50):
    """Return a random string usable as safe URL value (i.e. no encoding required)."""
    # See RFC-3986 (2.3. Unreserved Characters): http://www.ietf.org/rfc/rfc3986.txt
    unreserved_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~"
    return get_random_string(length, unreserved_chars)


def join_lazy(values, separator=""):
    if not separator:
        return string_concat(values)
    data = []
    for value in values:
        data.extend([value, separator])
    return string_concat(*data[:-1])


def static_url(path):
    clean_path = path.lstrip("/")
    if apps.is_installed("django.contrib.staticfiles"):
        from django.contrib.staticfiles.storage import staticfiles_storage
        return staticfiles_storage.url(clean_path)
    else:
        return urljoin(settings.STATIC_URL, quote(clean_path))
