import django_filters as filters

from ingupdong.models import RecordingBoard, TrendingBoard, Video


class RecordingFilterSet(filters.FilterSet):
    month = filters.NumberFilter(field_name='date', lookup_expr='month', required=True)
    year = filters.NumberFilter(field_name='date', lookup_expr='year', required=True)
    
    class Meta:
        model = RecordingBoard
        fields = ['month', 'year']


class VideoFilterSet(filters.FilterSet):
    channel_id = filters.NumberFilter(field_name='channel_id', lookup_expr='exact', required=True)

    class Meta:
        model = Video
        fields = ['channel_id']
