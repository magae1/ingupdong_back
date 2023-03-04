from rest_framework import serializers
from ingupdong.models import Channel, Video, RecordingBoard, TrendingBoard
from django.core.exceptions import ObjectDoesNotExist


YOUTUBE_URL = "https://www.youtube.com/"


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingBoard
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['handle'] = YOUTUBE_URL + data['handle']
        return data


class VideoSerializer(serializers.ModelSerializer):
    channel = serializers.StringRelatedField(many=False)

    class Meta:
        model = Video
        exclude = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['url'] = YOUTUBE_URL + data['url']
        return data


class TrendingSerializer(serializers.ModelSerializer):
    video = VideoSerializer(many=False, read_only=True)

    class Meta:
        model = TrendingBoard
        exclude = ['id', 'record']


class WithPrevTrendingSerializer(TrendingSerializer):
    prev_rank = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = TrendingBoard
        exclude = ['id', 'record']

    def get_prev_rank(self, obj):
        try:
            prev_date = RecordingBoard.objects.all()[1]
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

