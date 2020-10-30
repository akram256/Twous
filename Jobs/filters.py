from django_filters import FilterSet
from django_filters import rest_framework as filters
from .models import JobCategory



class JobCategoryFilter(FilterSet):
    """
    Create a filter class that inherits from FilterSet. This class will help
    us search for job categories using specified fields.
    """
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = JobCategory
        fields = (
            'name',
        )
