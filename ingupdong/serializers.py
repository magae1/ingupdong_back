from rest_framework import serializers
from ingupdong.models import Channel, Video, RecordingBoard, TrendingBoard
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import TruncDate


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


class TrendingWithRecordSerializer(SimpleTrendingSerializer):
    day = serializers.SlugRelatedField(many=False, read_only=True,
                                       slug_field='record_at', source='record')

    class Meta:
        model = TrendingBoard
        fields = ['day', 'rank', 'views']


class PrevAndNextRecordingSerializer(serializers.ModelSerializer):
    prev_record = serializers.SerializerMethodField(allow_null=True)
    next_record = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = RecordingBoard
        fields = '__all__'

    def get_prev_record(self, obj):
        try:
            query = RecordingBoard.objects.filter(record_at__lt=obj.record_at).last()
            data = RecordingSerializer(query).data
        except ObjectDoesNotExist:
            return None
        return data

    def get_next_record(self, obj):
        try:
            query = RecordingBoard.objects.filter(record_at__gt=obj.record_at).first()
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
            query = TrendingBoard.objects.select_related('video').filter(video__channel=obj).last()
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
            prev_date = RecordingBoard.objects.filter(record_at__lt=obj.record.record_at).last()
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
        record_objs = TrendingBoard.objects.filter(video=obj).select_related('record')\
            .annotate(record_date=TruncDate('record__record_at')).values('record_date')
        print(record_objs)
        result = []
        prev_date = None
        for obj in record_objs:
            cur_date = obj['record_date']
            if prev_date is None or prev_date != cur_date:
                result.append(cur_date)
            prev_date = cur_date
        return result
    

class VideoWithRecordAtSerializer(SimpleVideoSerializer):
    initial_record = serializers.SerializerMethodField(allow_null=False)

    class Meta:
        model = Video
        fields = '__all__'
        ordering = ['-id']

    def get_initial_record(self, obj):
        record_obj = TrendingBoard.objects.filter(video=obj)\
            .select_related('record').earliest('record').record
        data = RecordingSerializer(record_obj, many=False).data
        return data.get('record_at')
