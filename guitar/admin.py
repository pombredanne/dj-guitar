from django.contrib import admin
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _  # , pgettext_lazy as __


class BaseModelAdmin(admin.ModelAdmin):
    """Base ``ModelAdmin`` for ``AbstractBaseModel`` child classes."""

    # List view
    list_display = ["id"]
    search_fields = ["id"]

    # Change view
    fieldsets = [
        [capfirst(_("system")), {
            "classes": ["grp-collapse grp-closed"],
            "fields": ["id"],
        }],
    ]
    readonly_fields = ["id"]
    empty_value_display = ""  # __("admin empty value", "(empty)")
