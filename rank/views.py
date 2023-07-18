from rest_framework.generics import ListAPIView

from .models import ScoreOnChannel
from .serializers import ScoreOnChannelSerializer


class Ranking(ListAPIView):
    queryset = ScoreOnChannel.objects.all()
    serializer_class = ScoreOnChannelSerializer
    
    def get_queryset(self):
        query_set = self.queryset
        query_set = query_set.order_by('-score')[:12]
        return query_set
    