import django_filters as filters

from .models import RecordingBoard


class RecordingFilterSet(filters.FilterSet):
    month = filters.NumberFilter(field_name='record_at', lookup_expr='month', required=True)
    year = filters.NumberFilter(field_name='record_at', lookup_expr='year', required=True)
    
    class Meta:
        model = RecordingBoard
        fields = ['month', 'year']

