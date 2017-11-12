from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from . import urls_middlewares


urlpatterns = [
    url(r"^middlewares/", include(urls_middlewares, namespace="middlewares")),
]
