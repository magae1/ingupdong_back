from rest_framework import viewsets,filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, Http404

from ingupdong.models import TrendingBoard, RecordingBoard, Channel
from ingupdong.seiralizers import TrendingSerializer, RecordingSerializer, \
    PrevAndNextRecordingSerializer, ChannelSerializer
from ingupdong.filters import RecordingFilterSet, TrendingFilterSet


class TrendPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'size'
    offset_query_param = 'offset'
    max_limit = 50


class TrendingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingBoard.objects.all()
    serializer_class = TrendingSerializer
    filterset_class = TrendingFilterSet
    pagination_class = TrendPagination

    def list(self, request):
        raise Http404("잘못된 요청입니다.")

    def retrieve(self, request, pk='latest'):
        if pk == 'latest':
            trend_query = TrendingBoard.objects.filter(record=RecordingBoard.objects.latest())
        else:
            record_query = RecordingBoard.objects.all()
            record_obj = get_object_or_404(record_query, pk=pk)
            trend_query = TrendingBoard.objects.filter(record=record_obj)
        page = self.paginate_queryset(trend_query)
        if page is not None:
            serializer = TrendingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TrendingSerializer(trend_query, many=True)
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
        elif not pk.isnumeric():
            raise Http404("잘못된 요청입니다.")
        record_obj = get_object_or_404(query, pk=pk)
        serializer = PrevAndNextRecordingSerializer(record_obj, many=False)
        return Response(serializer.data)


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

