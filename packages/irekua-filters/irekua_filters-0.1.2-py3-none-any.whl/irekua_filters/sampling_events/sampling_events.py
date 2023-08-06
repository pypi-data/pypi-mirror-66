from django import forms
from django.db import models
from django.utils.translation import gettext as _

from django_filters import FilterSet
from django_filters import DateFilter
from django_filters import BooleanFilter

from irekua_database.models import SamplingEvent


def get_queryset(f):
    return f.target_field.model.objects.all()


class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())

    class Meta:
        model = SamplingEvent
        fields = {
            'sampling_event_type': ['exact'],
            'collection': ['exact'],
            'created_on': ['lt', 'gt'],
            'ended_on': ['lt', 'gt'],
            'started_on': ['lt', 'gt'],
            'collection_site': ['exact'],
            'collection_site__site': ['exact'],
            'collection_site__internal_id': ['icontains'],
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'samplingeventdevice__collection_device__physical_device': ['exact'],
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            },
        }

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(created_by=user)
        return queryset


search_fields = (
    'sampling_event_type__name',
    'collection_site__internal_id',
    'collection_site__site__name',
    'collection_site__site__locality__name',
    'collection__name',
)


ordering_fields = (
    ('created_on', _('added on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on')),
)
