from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet
from django_filters import DateFilter
from django_filters import BooleanFilter

from irekua_database.models import Item


class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())
    class Meta:
        model = Item
        fields = {
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'created_by__institution__institution_name': ['icontains'],
            'created_by__institution__institution_code': ['exact'],
            'created_by__institution__country': ['icontains'],
            'sampling_event_device': ['exact'],
            'sampling_event_device__collection_device__physical_device': ['exact'],
            'sampling_event_device__sampling_event__collection_site': ['exact'],
            'sampling_event_device__collection_device': ['exact'],
            'sampling_event_device__sampling_event': ['exact'],
            'sampling_event_device__sampling_event__collection_site__site': ['exact'],
            'item_type': ['exact'],
            'created_on': ['gt', 'lt'],
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            }
        }

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(created_by=user)
        return queryset

search_fields = (
    'item_type__name',
    'created_by__username',
    'created_by__first_name',
    'created_by__last_name',
    'sampling_event_device__collection_device__internal_id',
    'sampling_event_device__sampling_event__collection_site__internal_id',
    'annotation__labels__value'
)


ordering_fields = (
    ('captured_on', _('captured on')),
    ('created_on', _('added on')),
    ('filesize', _('filesize'))
)
