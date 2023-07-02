from django.db import models, transaction


class Channel(models.Model):
    name = models.CharField(max_length=150)
    handle = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'channel'

    def __str__(self):
        return f'[{self.id}]:{self.name}'


class Video(models.Model):
    title = models.CharField(max_length=120)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='channel')
    url = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video'
        
    def __str__(self):
        return f'{self.title}'


class RecordingBoard(models.Model):
    record_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recording'
        get_latest_by = ['record_at']
        ordering = ['record_at']
        
    def __str__(self):
        return self.record_at


class TrendingManager(models.Manager):
    @transaction.atomic
    def create_trending(self, rank, title, url, views, channel_name, handle, record_id):
        channel, create = Channel.objects.update_or_create(handle=handle, defaults={'name': channel_name})
        video, create = Video.objects.update_or_create(url=url,
                                                       defaults={
                                                        'channel': channel,
                                                        'title': title,
                                                       })
        return self.create(rank=rank, video=video, views=views, record_id=record_id)


class TrendingBoard(models.Model):
    rank = models.PositiveSmallIntegerField(unique=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='video')
    views = models.PositiveBigIntegerField()
    record = models.ForeignKey(RecordingBoard, on_delete=models.CASCADE)

    objects = models.Manager()
    customs = TrendingManager()

    class Meta:
        db_table = 'trending'
        ordering = ['record', 'rank']

    def __str__(self):
        return f'{self.record.record_at}[{self.rank}위]:{self.video.title}'
    