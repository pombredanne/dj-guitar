from django.conf import settings
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class GuitarMiddleware(MiddlewareMixin):
    """Provide extra information about the request and the current URL."""

    def process_request(self, request):
        request.ABSOLUTE_ROOT = request.build_absolute_uri("/").rstrip("/")
        request.ABSOLUTE_URL = request.build_absolute_uri()

        # Information about the current URL, used by the template tag ``core_tags.body_class``.
        request.ROUTE = self._get_route_info(request)

    def process_template_response(self, request, response):
        if getattr(response, "context_data", None) is None:
            response.context_data = {}
        response.context_data["DJANGO_ENV"] = settings.DJANGO_ENV
        response.context_data["ABSOLUTE_ROOT"] = request.ABSOLUTE_ROOT
        response.context_data["ABSOLUTE_URL"] = request.ABSOLUTE_URL
        return response

    def _get_route_info(self, request):
        """Return information about the current URL."""
        resolve_match = resolve(request.path)

        app_name = resolve_match.app_name    # The application namespace for the URL pattern that matches the URL.
        namespace = resolve_match.namespace  # The instance namespace for the URL pattern that matches the URL.
        url_name = resolve_match.url_name    # The name of the URL pattern that matches the URL.
        view_name = resolve_match.view_name  # Name of the view that matches the URL, incl. namespace if there's one.

        return {
            "app_name": app_name or None,
            "namespace": namespace or None,
            "url_name": url_name or None,
            "view_name": view_name or None,
        }
