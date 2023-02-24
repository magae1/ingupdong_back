from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from ingupdong.models import TrendingBoard, RecordingBoard
from ingupdong.seiralizers import TrendingSerializer, WithPrevTrendingSerializer, RecordingSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50


class TrendingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrendingSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        record_id = self.request.query_params.get('date_id')
        queryset = TrendingBoard.objects.filter(record=RecordingBoard.objects.latest())
        if record_id is not None:
            queryset = TrendingBoard.objects.filter(record_id=record_id)
        return queryset

    @action(detail=False)
    def latest_trend(self, request):
        query_set = TrendingBoard.objects.filter(record=RecordingBoard.objects.latest())
        page = self.paginate_queryset(query_set)
        if page is not None:
            serializer = WithPrevTrendingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = WithPrevTrendingSerializer(query_set, many=True)
        return Response(serializer.data)


class RecordingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordingBoard.objects.all()
    serializer_class = RecordingSerializer

