from django.apps import AppConfig
from django.utils.text import capfirst
from django.utils.translation import pgettext_lazy as __


class GuitarConfig(AppConfig):

    name = "guitar"
    verbose_name = capfirst(__("Django app", "guitar"))
