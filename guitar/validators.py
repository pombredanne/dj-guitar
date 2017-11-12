from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator as DjangoBaseValidator
from django.utils.deconstruct import deconstructible

from .utils import join_lazy


@deconstructible
class BaseValidator(DjangoBaseValidator):
    """Extend Django's ``BaseValidator`` with getters for error message parameters."""
    # Source: https://github.com/django/django/blob/1.11.7/django/core/validators.py#L312

    def __call__(self, value):
        self.value = value
        self.cleaned = self.clean(value)
        if self.compare(self.cleaned, self.limit_value):
            raise ValidationError(self.message, code=self.code, params=self.get_error_params())

    def get_error_params(self):
        """Return the parameters to format the error message."""
        return {
            "limit_value": self.get_limit_value_string(),
            "show_value": self.cleaned,
            "value": self.value,
        }

    def get_limit_value_string(self):
        """Return the list of allowed choices as a string."""
        if isinstance(self.limit_value, (list, tuple)):
            return join_lazy(self.limit_value, separator=", ")
        if isinstance(self.limit_value, dict):
            return join_lazy([v for k, v in self.limit_value.items()], separator=", ")
        return self.limit_value
