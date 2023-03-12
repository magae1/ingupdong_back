import django_filters as filters
from ingupdong.models import RecordingBoard, TrendingBoard


class RecordingFilterSet(filters.FilterSet):
    month = filters.NumberFilter(field_name='date', lookup_expr='month', required=True)

    class Meta:
        model = RecordingBoard
        fields = ['month']


class TrendingFilterSet(filters.FilterSet):
    class Meta:
        model = TrendingBoard
        fields = ['rank']

