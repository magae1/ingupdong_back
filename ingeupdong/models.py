from django.db import models
from .managers import RecordingManager, TrendingManager


class Channel(models.Model):
    name = models.CharField(max_length=150,
                            help_text='채널명')
    handle = models.CharField(max_length=50, unique=True,
                              help_text='채널 핸들명')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='채널의 첫 크롤링 날짜')

    class Meta:
        db_table = 'channel'

    def __str__(self):
        return f'[{self.id}]:{self.name}'


class Video(models.Model):
    title = models.CharField(max_length=120,
                             help_text='동영상 제목')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='channel')
    url = models.CharField(max_length=50, unique=True,
                           help_text='동영상 url')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='영상의 첫 크롤링 날짜')

    class Meta:
        db_table = 'video'
        get_latest_by = ['created_at']
        
    def __str__(self):
        return f'{self.title}'


class RecordingBoard(models.Model):
    record_at = models.DateTimeField(auto_now=True, help_text='크롤링 날짜')

    class Meta:
        db_table = 'recording'
        get_latest_by = ['record_at']
        ordering = ['record_at']
    
    objects = models.Manager()
    customs = RecordingManager()
    
    def __str__(self):
        return f'{self.record_at.strftime("%y년 %m월 %d일 %H:%M")}'


class TrendingBoard(models.Model):
    rank = models.PositiveSmallIntegerField(unique=False,
                                            help_text='인급동 순위')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='video')
    views = models.PositiveBigIntegerField(help_text='영상 조회수')
    record = models.ForeignKey(RecordingBoard, on_delete=models.CASCADE)

    objects = models.Manager()
    customs = TrendingManager()

    class Meta:
        db_table = 'trending'
        ordering = ['record', 'rank']

    def __str__(self):
        return f'{self.record.record_at}[{self.rank}위]:{self.video.title}'
    