from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from irekua_database.models import PhysicalDevice


class Filter(FilterSet):

    class Meta:
        model = PhysicalDevice
        fields = {
            'serial_number': ['exact', 'icontains'],
            'device__brand__name': ['exact', 'icontains'],
            'device__model': ['exact', 'icontains'],
            'bundle': ['exact'],
            'identifier': ['exact', 'icontains'],
            'created_on': ['lt', 'gt']
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            }
        }


search_fields = (
    'device__brand__name',
    'device__model',
    'serial_number',
    'device__device_type__name',
    'identifier',
)


ordering_fields = (
    ('created_on', _('added on')),
    ('serial_number', _('serial number')),
    ('identifier', _('custom id')),
    ('device__brand__name', _('brand')),
    ('device__model', _('model')),
)
