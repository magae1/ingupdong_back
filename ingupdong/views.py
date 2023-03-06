from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, Http404

from ingupdong.models import TrendingBoard, RecordingBoard
from ingupdong.seiralizers import TrendingSerializer, WithPrevTrendingSerializer, RecordingSerializer, \
    NavRecordingSerializer
from ingupdong.filters import RecordingFilterSet, TrendingFilterSet


class TrendPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'size'
    offset_query_param = 'offset'
    max_limit = 50


class TrendingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingBoard.objects.all()
    serializer_class = WithPrevTrendingSerializer
    filterset_class = TrendingFilterSet
    pagination_class = TrendPagination

    def list(self, request):
        raise Http404("잘못된 요청입니다.")

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
        record_query = RecordingBoard.objects.all()
        record_obj = get_object_or_404(record_query, pk=pk)
        trend_query = TrendingBoard.objects.filter(record=record_obj)
        page = self.paginate_queryset(trend_query)
        if page is not None:
            serializer = WithPrevTrendingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = WithPrevTrendingSerializer(trend_query, many=True)
        return Response(serializer.data)


class RecordingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordingBoard.objects.all()
    serializer_class = RecordingSerializer
    filterset_class = RecordingFilterSet
    pagination_class = TrendPagination

    @action(detail=True, methods=['get'], name='Get previous and next record')
    def details(self, request, pk=None):
        query = RecordingBoard.objects.all()
        if pk == 'latest':
            pk = RecordingBoard.objects.latest().id
        record_obj = get_object_or_404(query, pk=pk)
        serializer = NavRecordingSerializer(record_obj, many=False)
        return Response(serializer.data)


