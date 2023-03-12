from rest_framework import serializers
from ingupdong.models import Channel, Video, RecordingBoard, TrendingBoard
from django.core.exceptions import ObjectDoesNotExist


YOUTUBE_URL = "https://www.youtube.com/"


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingBoard
        fields = '__all__'


class PrevAndNextRecordingSerializer(serializers.ModelSerializer):
    prev_record = serializers.SerializerMethodField(allow_null=True)
    next_record = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = RecordingBoard
        fields = '__all__'

    def get_prev_record(self, obj):
        try:
            data = RecordingBoard.objects.filter(date__lt=obj.date).order_by('-date', '-time').first()
            data = RecordingSerializer(data).data
        except ObjectDoesNotExist:
            return None
        return data

    def get_next_record(self, obj):
        try:
            data = RecordingBoard.objects.filter(date__gt=obj.date).order_by('date', 'time').first()
            data = RecordingSerializer(data).data
        except ObjectDoesNotExist:
            return None
        return data


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['handle'] = YOUTUBE_URL + data['handle']
        return data


class VideoSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(many=False)

    class Meta:
        model = Video
        exclude = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['url'] = YOUTUBE_URL + data['url']
        return data


class TrendingSerializer(serializers.ModelSerializer):
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

