from rest_framework import serializers

from .models import ScoreOnChannel
from ingeupdong.serializers import ChannelSerializer


class ScoreOnChannelSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    
    class Meta:
        model = ScoreOnChannel
        fields = ['channel', 'score']
        