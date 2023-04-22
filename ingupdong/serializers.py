from rest_framework import serializers
from ingupdong.models import Channel, Video, RecordingBoard, TrendingBoard
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F


YOUTUBE_URL = "https://www.youtube.com/"


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingBoard
        fields = '__all__'


class SimpleVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'url']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['url'] = YOUTUBE_URL + data['url']
        return data


class SimpleTrendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingBoard
        fields = ['rank', 'views']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class VideoSerializer(SimpleVideoSerializer):
    channel = ChannelSerializer(many=False)

    class Meta:
        model = Video
        fields = '__all__'


class TrendingSerializer(SimpleTrendingSerializer):
    video = SimpleVideoSerializer(many=False, read_only=True)
    record = RecordingSerializer(many=False, read_only=True)

    class Meta:
        model = TrendingBoard
        fields = '__all__'


class PrevAndNextRecordingSerializer(serializers.ModelSerializer):
    prev_record = serializers.SerializerMethodField(allow_null=True)
    next_record = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = RecordingBoard
        fields = '__all__'

    def get_prev_record(self, obj):
        try:
            query = RecordingBoard.objects.filter(date__lt=obj.date).order_by('-date', '-time').first()
            data = RecordingSerializer(query).data
        except ObjectDoesNotExist:
            return None
        return data

    def get_next_record(self, obj):
        try:
            query = RecordingBoard.objects.filter(date__gt=obj.date).order_by('date', 'time').first()
            data = RecordingSerializer(query).data
        except ObjectDoesNotExist:
            return None
        return data


class ChannelWithLatestTrendSerializer(ChannelSerializer):
    latest_video = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Channel
        fields = '__all__'

    def get_latest_video(self, obj):
        try:
            query = TrendingBoard.objects.select_related('video').filter(video__channel=obj).first()
            data = SimpleVideoSerializer(query.video).data
        except ObjectDoesNotExist:
            return None
        return data


class TrendingWithPrevSerializer(serializers.ModelSerializer):
    video = VideoSerializer(many=False, read_only=True)
    prev_trend = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = TrendingBoard
        exclude = ['id', 'record']

    def get_prev_trend(self, obj):
        try:
            prev_date = RecordingBoard.objects.filter(date__lt=obj.record.date).order_by('-date', '-time').first()
            prev_trend = TrendingBoard.objects.get(record=prev_date,
                                                   video=obj.video)
        except ObjectDoesNotExist:
            prev_trend = None
        except IndexError:
            prev_trend = None

        if prev_trend is None:
            return None
        return {
            'rank': prev_trend.rank,
            'views': prev_trend.views
        }


class VideoWithRecordsSerializer(VideoSerializer):
    records = serializers.SerializerMethodField(allow_null=False)

    class Meta:
        model = Video
        exclude = ['id']

    def get_records(self, obj):
        record_objs = TrendingBoard.objects.filter(video=obj)\
            .select_related('record').values_list('record__date', flat=True).reverse()
        return record_objs.all()


class VideoWithRecordAtSerializer(SimpleVideoSerializer):
    record_at = serializers.SerializerMethodField(allow_null=False)

    class Meta:
        model = Video
        fields = '__all__'
        ordering = ['-id']

    def get_record_at(self, obj):
        record_obj = TrendingBoard.objects.filter(video=obj)\
            .select_related('record').latest('record').record
        data = RecordingSerializer(record_obj, many=False).data
        return data.get('date')
