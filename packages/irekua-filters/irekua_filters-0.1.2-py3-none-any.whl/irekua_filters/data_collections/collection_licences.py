from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter
from django_filters import BooleanFilter

from irekua_database.models import Licence


class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())
    class Meta:
        model = Licence
        fields = {
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'licence_type': ['exact'],
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
            return queryset.filter(physical_device__created_by=user)
        return queryset

search_fields = (
    'created_by__username',
    'created_by__first_name',
    'created_by__last_name',
    'licence_type__name'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('licence_type', _('licence type')),
)
