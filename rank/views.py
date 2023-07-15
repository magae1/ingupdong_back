from django.db.models import Sum
from rest_framework.generics import ListAPIView

from ingeupdong.models import Channel
from ingeupdong.serializers import ChannelSerializer


class Ranking(ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    
    def get_queryset(self):
        query_set = self.queryset
        query_set = query_set.annotate(total_score=Sum('scores__score'))
        query_set = query_set.order_by('-total_score')[:10]
        return query_set
    