from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from ingupdong.models import TrendingBoard, RecordingBoard
from ingupdong.seiralizers import TrendingSerializer, WithPrevTrendingSerializer, RecordingSerializer
from ingupdong.filters import RecordingFilterSet, TrendingFilterSet


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class TrendingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingBoard.objects.all()
    serializer_class = TrendingSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = TrendingFilterSet

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
    filterset_class = RecordingFilterSet

