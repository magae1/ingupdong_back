from rest_framework import viewsets, filters, generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, Http404

from ingupdong.models import TrendingBoard, RecordingBoard, Channel, Video
from ingupdong.serializers import TrendingWithPrevSerializer, RecordingSerializer, \
    PrevAndNextRecordingSerializer, ChannelSerializer, ChannelWithLatestTrendSerializer, \
    VideoWithRecordsSerializer, VideoWithRecordAtSerializer
from ingupdong.filters import RecordingFilterSet, VideoFilterSet


class TrendPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'size'
    offset_query_param = 'offset'
    max_limit = 50


class VideoPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'
    max_page_size = 10


class TrendingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingBoard.objects.all()
    serializer_class = TrendingWithPrevSerializer
    pagination_class = TrendPagination

    def list(self, request):
        raise Http404("잘못된 요청입니다.")

    def retrieve(self, request, pk=None):
        if pk == 'latest':
            trend_query = TrendingBoard.objects.filter(record=RecordingBoard.objects.latest())
        else:
            record_query = RecordingBoard.objects.all()
            record_obj = get_object_or_404(record_query, pk=pk)
            trend_query = TrendingBoard.objects.filter(record=record_obj)
        serializer = self.get_serializer_class()
        page = self.paginate_queryset(trend_query)
        if page is not None:
            data = serializer(page, many=True).data
            return self.get_paginated_response(data)
        data = serializer(trend_query, many=True).data
        return Response(data)


class RecordingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordingBoard.objects.all()
    serializer_class = RecordingSerializer
    filterset_class = RecordingFilterSet

    def retrieve(self, request, pk=None):
        query = self.get_queryset()
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
    pagination_class = VideoPagination
    
    def list(self, request):
        raise Http404("잘못된 요청입니다.")
    
    def retrieve(self, request, pk=None):
        query = self.get_queryset()
        serializer = ChannelWithLatestTrendSerializer
        channel_obj = get_object_or_404(query, pk=pk)
        data = serializer(channel_obj).data
        return Response(data)
    
    @action(detail=True, methods=['get'], name='get videos on the channel')
    def videos(self, request, pk=None):
        query = Video.objects.filter(channel_id=pk).order_by('-id')
        # page = self.paginate_queryset(query)
        # if page is not None:
        #     serializer = VideoWithRecordAtSerializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = VideoWithRecordAtSerializer(query, many=True)
        return Response(serializer.data)


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoWithRecordAtSerializer
    
    def list(self, request, *args, **kwargs):
        raise Http404()

    def retrieve(self, request, pk=None):
        query = self.get_queryset()
        serializer = VideoWithRecordsSerializer
        video_obj = get_object_or_404(query, pk=pk)
        data = serializer(video_obj).data
        return Response(data)


class ChannelListView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    