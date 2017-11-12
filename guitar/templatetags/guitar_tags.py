# Best practice: Name all functions for filters/tags/helpers with the suffixes "_filter", "_tag", and "_helper".

from os.path import join
from urllib.parse import urljoin

from django import template
from django.conf import settings

from ..utils import static_url


register = template.Library()


@register.simple_tag(name="body_class", takes_context=True)
def body_class_tag(context, **kwargs):
    """
    Return CSS "class" attributes for <body>.

    Allows to provide a CSS namespace using urlpatterns namespace (as ``.ns-*``) and view name (as ``.vw-*``).
    Requires: ``apps.core.middlewares.CoreMiddleware``.
    """
    request = context.get("request")
    if not hasattr(request, "ROUTE"):
        return ""

    css_classes = []

    namespace = request.ROUTE["namespace"]
    if namespace:
        namespace = namespace.replace("_", "-")
        css_classes.append("ns-{}".format(namespace))

    view = request.ROUTE["url_name"]  # Use ``url_name`` as ``view_name`` includes the namespace.
    if view:
        view = view.replace("_", "-")
        css_classes.append("vw-{}".format(view))

    return " ".join(css_classes)


@register.simple_tag(name="set", takes_context=True)
def set_tag(context, name, value):
    """Allow to define a variable directly in a template."""
    context[name] = value
    return ""


@register.simple_tag(name="settings")
def settings_tag(key, default=None):
    """Retrieve values from settings."""
    return getattr(settings, key, default)


@register.simple_tag(name="static_absolute", takes_context=True)
def static_absolute_tag(context, path):
    """Return the absolute URL of a static file."""
    request = context.get("request")
    return urljoin(request.ABSOLUTE_ROOT, static_url(path))


@register.simple_tag(name="static_cdn")
def static_cdn_tag(path, cdn, cdn_only=False):
    """Return the URL of a static file, with handling of offline mode."""
    clean_path = path.lstrip("/")
    if getattr(settings, "OFFLINE", False):
        return static_url(join("vendor", clean_path))
    elif cdn_only:
        return cdn
    return urljoin(cdn, clean_path)