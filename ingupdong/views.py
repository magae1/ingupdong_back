from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from ingupdong.models import TrendingBoard, RecordingBoard
from ingupdong.seiralizers import TrendingSerializer, WithPrevTrendingSerializer, RecordingSerializer, NavRecordingSerializer
from ingupdong.filters import RecordingFilterSet, TrendingFilterSet


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class TrendingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingBoard.objects.all()
    serializer_class = WithPrevTrendingSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = TrendingFilterSet

    @action(detail=False, url_path='latest')
    def latest_trend(self, request):
        query_set = TrendingBoard.objects.filter(record=RecordingBoard.objects.latest())
        page = self.paginate_queryset(query_set)
        if page is not None:
            serializer = WithPrevTrendingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = WithPrevTrendingSerializer(query_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query_set = TrendingBoard.objects.filter(record_id=pk)
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

    @action(detail=True, methods=['get'], name='Get previous and next record')
    def details(self, request, pk=None):
        query = RecordingBoard.objects.all()
        if pk == 'latest':
            pk = RecordingBoard.objects.latest().id
        record_obj = get_object_or_404(query, pk=pk)
        serializer = NavRecordingSerializer(record_obj, many=False)
        return Response(serializer.data)


