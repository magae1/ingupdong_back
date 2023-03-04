import django_filters as filters
from ingupdong.models import RecordingBoard, TrendingBoard


class RecordingFilterSet(filters.FilterSet):
    month = filters.DateFromToRangeFilter(field_name='date', label='month')

    class Meta:
        model = RecordingBoard
        fields = ['date']


class TrendingFilterSet(filters.FilterSet):
    record_at = filters.ModelChoiceFilter(queryset=RecordingBoard.objects.all(), label="record_at")

    class Meta:
        model = TrendingBoard
        fields = ['rank']

