# -*- coding: utf8 -*-

from django.forms.forms import Form
from django.forms.fields import CharField, MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.contenttypes.models import ContentType

from fokus.search.models import Index

def initial_types():
    return [ContentType.objects.get_for_model(m).id for m in Index.searchable_models()]

class SearchForm(Form):
    q = CharField(label='Søkekriterier', required=True)
    types = MultipleChoiceField(label='Søk blant',
                                widget=CheckboxSelectMultiple(),
                                initial=initial_types(),
                                choices=[(ContentType.objects.get_for_model(m).id, m._meta.verbose_name_plural.title())
                                            for m in Index.searchable_models()],
                                required=False)
    