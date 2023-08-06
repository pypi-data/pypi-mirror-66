import re

from django.urls import reverse
from django.utils.http import urlencode
from dal import autocomplete


def get_autocomplete_widget(model=None, name=None, multiple=False, attrs=None, **kwargs):
    if name is None:
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', model.__name__).lower() + 's'

    view_name = 'irekua_autocomplete:{name}_autocomplete'.format(name=name)
    url = reverse(view_name)

    if kwargs:
        url = '{}?{}'.format(url, urlencode(kwargs))

    if attrs is None:
        attrs = {
            'style': 'width: 100%;'
        }

    if multiple:
        return autocomplete.ModelSelect2Multiple(url=url, attrs=attrs)

    return autocomplete.ModelSelect2(url=url, attrs=attrs)
