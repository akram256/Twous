from django_filters import FilterSet
from django_filters import rest_framework as filters
from Auth.models import Profile

class ProviderFilter(FilterSet):
    """
    Create a filter class that inherits from FilterSet. This class will help
    us search for Providers using specified fields.
    """
    phone_no = filters.CharFilter(lookup_expr='icontains')
    first_name=filters.CharFilter(lookup_expr='icontains')
    last_name=filters.CharFilter(lookup_expr='icontains')
    email=filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = (
            'phone_no','first_name', 'last_name', 'email'
        )