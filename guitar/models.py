import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModelMixin(object):
    """
    Add `AbstractBaseModel` features.

    Allows to add these features in classes that cannot directly inherit from a ``Model`` class.
    """

    pass


class AbstractBaseModel(BaseModelMixin, models.Model):
    """
    Base Model.

    Uses a UUID as id/primary key field.
    """

    id = models.UUIDField(_("ID"), default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True

    @property
    def uuid(self):
        return str(self.pk)
