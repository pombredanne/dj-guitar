from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices as ModelUtilsChoices

from ..validators import BaseValidator
from . import join_lazy


@deconstructible
class ChoicesValidator(BaseValidator):
    """Validate that the input is in the available choices, otherwise raise ValidationError."""
    # @TODO: Was working at MQ. Doesn't seem to work.
    # from apps.core.utils.choices import *
    # c = Choices((1, "SingleValue", "Single value"), (2, "Division", "Division"))
    # c.validator(c.SingleValue)
    # c.validator("SingleValue")
    # c.validator("Single value")

    message = _("Value '%(show_value)s' is not allowed. Available choices are: '%(limit_value)s'.")
    code = "invalid_choice"

    def compare(self, value, allowed_choices):
        """Return True if the value is *NOT* valid (i.e. if it's not in the allowed choices)."""
        return allowed_choices is not None and value not in allowed_choices

    def get_limit_value_string(self):
        """Return the list of allowed choices as a string."""
        return join_lazy([v for k, v in self.limit_value], separator=", ")


class Choices(ModelUtilsChoices):
    """
    Add some functionalities to ``django-model-utils.Choice``.

    Choices can be created as follows:
        - Choices(("database-value"))  # Also used as human-readable presentation.
        - Choices(("database-value", "Human-readable presentation"))
        - Choices(("database-value", "PythonIdentifier", "Human-readable presentation"))

    Terminology:
        - key = database value
        - human key = Python identifier
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ``_doubles``: List of choices as (database value, human-readable presentation) - can include optgroups.
        # Example: [("database-value", "Human-readable presentation")]
        # Source: https://github.com/jazzband/django-model-utils/blob/3.0.0/model_utils/choices.py#L49
        self.validator = ChoicesValidator(self._doubles)

    def get_human_key(self, key):
        """Return the human key (aka Python identifier) of a key (aka database value)."""
        # ``_identifier_map``: Dictionary mapping Python identifier to database value.
        # Example: {"PythonIdentifier": "database-value"}
        # Source: https://github.com/jazzband/django-model-utils/blob/3.0.0/model_utils/choices.py#L53
        for human_key, k in self._identifier_map.items():
            if k == key:
                return human_key
        raise KeyError(key)


class ChoiceModelField(models.PositiveSmallIntegerField):
    """A model field for ``django-model-utils.Choice`` (small integer triplets)."""

    description = _("Choice")

    def __init__(self, choices, **kwargs):
        kwargs["choices"] = choices
        kwargs.setdefault("db_index", True)
        super().__init__(**kwargs)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        super().contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, "get_{}_human_key".format(name), curry(cls._get_FIELD_human_key, field=self))
