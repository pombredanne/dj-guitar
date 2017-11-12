"""Routes for test cases."""

from django.conf.urls import url
from django.views.generic.base import TemplateView


app_name = "middlewares_app"
urlpatterns = [
    url(r"^guitar-middleware/$", TemplateView.as_view(), name="guitar_middleware")
]
