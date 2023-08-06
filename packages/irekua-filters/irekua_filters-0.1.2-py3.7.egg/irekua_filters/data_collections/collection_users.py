from django.utils.translation import gettext as _
from django_filters import FilterSet

from irekua_database.models import CollectionUser


class Filter(FilterSet):
    class Meta:
        model = CollectionUser
        fields = {
            'role': ['exact'],
            'user': ['exact'],
            'user__institution': ['exact'],
            'user__institution__institution_name': ['icontains'],
            'user__institution__institution_code': ['icontains'],
            'user__institution__country': ['exact'],
            'user__first_name': ['icontains'],
            'user__last_name': ['icontains'],
            'user__username': ['icontains'],
            'user__email': ['icontains'],
            'created_on': ['gt', 'lt']
        }


search_fields = (
    'user__first_name',
    'user__last_name',
    'user__username',
    'user__email',
    'user__institution__institution_name',
    'user__institution__institution_code'
)

ordering_fields = (
    ('created_on', _('added on')),
    ('user__first_name', _('first name')),
    ('user__last_name', _('last name')),
    ('user__username', _('username')),
)
