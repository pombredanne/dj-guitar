from copy import deepcopy

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import six
from django.utils.html import format_html


ADMIN_GLOBAL_PAGES = ("app_list", "view_on_site")
ADMIN_LIST_PAGES = ("changelist", "add")
ADMIN_DETAIL_PAGES = ("change", "delete", "history")
ADMIN_ALL_PAGES = ADMIN_GLOBAL_PAGES + ADMIN_LIST_PAGES + ADMIN_DETAIL_PAGES


def csv_list(models, attr, link=False, separator=", "):
    """Return a comma-separated list of models, optionaly with a link."""
    values = []
    for model in models:
        value = getattr(model, attr)
        if link and hasattr(model, "get_admin_url") and callable(model.get_admin_url):
            value = '<a href="{}">{}</a>'.format(model.get_admin_url(), value)
        values.append(value)
    return separator.join(values)


def get_admin_url(obj, page=None):
    """Return the URL to admin pages for this object."""
    if page is None:
        page = "change"
    if page not in ADMIN_ALL_PAGES:
        raise ValueError("Invalid page name '{}'. Available pages are: {}.".format(page, ADMIN_ALL_PAGES))

    content_type = ContentType.objects.get_for_model(obj.__class__)

    if page in ADMIN_GLOBAL_PAGES:
        url_name = page
    else:
        url_name = "{}_{}_{}".format(content_type.app_label, content_type.model, page)

    if page == "app_list":
        url_args = (content_type.app_label,)
    elif page == "view_on_site":
        url_args = (content_type, obj._get_pk_val())
    elif page in ADMIN_DETAIL_PAGES:
        url_args = (obj._get_pk_val(),)
    else:
        url_args = None

    return reverse("admin:{}".format(url_name), args=url_args)


def get_admin_html_link(obj, label=None):
    return format_html('<a href="{}">{}</a>', get_admin_url(obj), label or obj)


# LISTS AND FIELDSETS MANIPULATION =====================================================================================

def combine_fields_dict(*args):
    combined = {}
    for arg in args:
        for k, v in arg.items():
            if k not in combined:
                combined[k] = []
            combined[k] = combined[k] + v
    return combined


def concat_fieldsets(*args):
    fieldsets = []
    fieldset_names = {}
    index = 0
    for arg in args:
        for fieldset in arg:
            name, content = list(fieldset)
            i = fieldset_names.get(name)
            if i:
                for k, v in content.items():
                    fieldsets[i][1][k] += v
            else:
                fieldset_names[name] = index
                fieldsets.append(deepcopy(fieldset))
            index += 1
    return fieldsets


def get_fieldset_index(fieldsets, index_or_name):
    """
    Return the index of a fieldset in the ``fieldsets`` list.

    Args:
        fieldsets (list): The original ``fieldsets`` list.
        index_or_name (int or str): The value of the reference element, or directly its numeric index.

    Returns:
        (int) The index of the fieldset in the ``fieldsets`` list.
    """
    if isinstance(index_or_name, six.integer_types):
        return index_or_name

    for key, value in enumerate(fieldsets):
        if value[0] == index_or_name:
            return key

    raise KeyError("Key not found: '{}'.".format(index_or_name))


def get_list_index(lst, index_or_name):
    """
    Return the index of an element in the list.

    Args:
        lst (list): The list.
        index_or_name (int or str): The value of the reference element, or directly its numeric index.

    Returns:
        (int) The index of the element in the list.
    """
    if isinstance(index_or_name, six.integer_types):
        return index_or_name

    return lst.index(index_or_name)


def replace_fields_in_fieldsets(fieldsets, fieldset_index_or_name, new_fields):
    fieldset_index = get_fieldset_index(fieldsets, fieldset_index_or_name)
    to_return = deepcopy(fieldsets)
    to_return[fieldset_index][1]["fields"] = new_fields
    return to_return


def insert_fields_in_fieldsets(fieldsets, fieldset_index_or_name, new_fields, field_index_or_name=None, after=True):
    """
    Return a copy of the ``fieldsets`` list with the new field(s) inserted.

    Args:
        fieldsets (list): The original ``fieldsets`` list.
        fieldset_index_or_name (int or str): The name of the reference fieldset, or directly its numeric index.
        new_fields (str or list of str): The field(s) to insert in the ``fieldsets`` list.
        field_index_or_name (int or str): The name of the reference field, or directly its numeric index.
                                          Default: None (=append).
        after (bool): Whether to insert the new elements before or after the reference element. Default: True.

    Returns:
        (list) A copy of the original ``fieldsets`` list containing the new field(s).
    """
    fieldset_index = get_fieldset_index(fieldsets, fieldset_index_or_name)
    fieldset_fields = fieldsets[fieldset_index][1]["fields"]

    try:
        field_index = get_list_index(fieldset_fields, field_index_or_name)
    except ValueError:
        field_index = None

    to_return = deepcopy(fieldsets)
    to_return[fieldset_index][1]["fields"] = list_insert(fieldset_fields, new_fields, field_index, after=after)
    return to_return


def list_insert(lst, new_elements, index_or_name=None, after=True):
    """
    Return a copy of the list with the new element(s) inserted.

    Args:
        lst (list): The original list.
        new_elements ("any" or list of "any"): The element(s) to insert in the list.
        index_or_name (int or str): The value of the reference element, or directly its numeric index.
                                    Default: None (=append).
        after (bool): Whether to insert the new elements before or after the reference element. Default: True.

    Returns:
        (list) A copy of the original list containing the new element(s).
    """
    if index_or_name is None:
        index = None
    else:
        try:
            index = get_list_index(lst, index_or_name)
        except ValueError:
            index = None

    to_return = lst[:]
    if index is None:  # Append.
        to_return += new_elements
    elif index == 0:  # Prepend.
        to_return = new_elements + to_return
    else:
        if after:
            index += 1
        to_return = to_return[:index] + new_elements + to_return[index:]
    return to_return
