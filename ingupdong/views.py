import datetime

import dateutil.parser
from dateutil.relativedelta import relativedelta

from rest_framework import viewsets, filters, generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, Http404
from django.db.models import Count

from ingupdong.models import TrendingBoard, RecordingBoard, Channel, Video
from ingupdong.serializers import TrendingWithPrevSerializer, RecordingSerializer, \
    PrevAndNextRecordingSerializer, ChannelSerializer, ChannelWithLatestTrendSerializer, \
    VideoWithRecordsSerializer, VideoWithRecordAtSerializer, TrendingWithRecordSerializer
from ingupdong.filters import RecordingFilterSet


class TrendPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'size'
    offset_query_param = 'offset'
    max_limit = 50


class VideoPagination(PageNumberPagination):
    page_size = 10
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
            date = RecordingBoard.objects.latest().record_at
        else:
            date = dateutil.parser.parse(pk)
        try:
            record_obj = query.filter(record_at__day=date.day,
                                      record_at__month=date.month,
                                      record_at__year=date.year,
                                      record_at__hour=date.hour).last()
        except RecordingBoard.DoesNotExist:
            raise Http404('일치하는 기록이 없습니다.')
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
        channel_obj = get_object_or_404(query, pk=pk)
        serializer = ChannelWithLatestTrendSerializer
        data = serializer(channel_obj).data
        return Response(data)
    
    @action(detail=True, methods=['get'], name='videos on the channel')
    def videos(self, request, pk=None):
        query = self.get_queryset()
        channel_obj = get_object_or_404(query, pk=pk)
        videos_query = Video.objects.filter(channel=channel_obj).order_by('-id')
        page = self.paginate_queryset(videos_query)
        if page is not None:
            serializer = VideoWithRecordAtSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = VideoWithRecordAtSerializer(videos_query, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], name='the number of videos on the channel')
    def count(self, request, pk=None):
        query = self.get_queryset()
        channel_obj = get_object_or_404(query, pk=pk)
        total_count = Video.objects.filter(channel=channel_obj).count()
        
        today = datetime.date.today()
        prev_date = today + relativedelta(days=-100)
        recent_records_obj = TrendingBoard.objects.all().select_related('record').filter(record__record_at__gt=prev_date) \
            .select_related('video').filter(video__channel=channel_obj)\
            .values('record__record_at').annotate(count=Count('video_id'))\
            .order_by('record__record_at').values('record__record_at', 'count')
        recent_records = [{'day': obj['record__record_at'], 'value': obj['count']} for obj in recent_records_obj]
        return Response({'total_count': total_count, 'recent_records': recent_records,
                         'start_date': prev_date, 'end_date': today})


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoWithRecordsSerializer
    
    def list(self, request, *args, **kwargs):
        raise Http404()

    def retrieve(self, request, pk=None):
        query = self.get_queryset()
        video_obj = get_object_or_404(query, pk=pk)
        serializer = self.get_serializer_class()
        data = serializer(video_obj).data
        return Response(data)
    
    @action(detail=True, methods=['get'], name="get video's views and rank")
    def graphed(self, request, pk=None):
        query = TrendingBoard.objects.filter(video_id=pk).order_by('id')
        serializer = TrendingWithRecordSerializer(query, many=True)
        return Response(serializer.data)


class ChannelListView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    