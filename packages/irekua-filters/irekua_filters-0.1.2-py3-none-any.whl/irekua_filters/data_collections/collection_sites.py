from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet
from django_filters import BooleanFilter

from irekua_database.models import CollectionSite


class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())
    class Meta:
        model = CollectionSite
        fields = {
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'site_type': ['exact'],
            'site': ['exact'],
            'site__altitude': ['gt', 'lt'],
            'site__latitude': ['gt', 'lt'],
            'site__longitude': ['gt', 'lt'],
            'site__name': ['icontains'],
            'site__locality': ['exact'],
            'site__locality__name': ['icontains'],
            'created_on': ['gt', 'lt']
        }

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(created_by=user)
        return queryset


search_fields = (
    'internal_id',
    'site__name',
    'site__locality__name',
    'site_type__name',
)

ordering_fields = (
    ('created_on', _('added on')),
    ('internal_id', _('internal id'))
)
