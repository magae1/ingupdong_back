from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=150)
    handle = models.CharField(max_length=50)

    class Meta:
        db_table = 'channel'
        unique_together = [['name', 'handle']]

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=120)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='channel')
    url = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'video'


class RecordingBoard(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    class Meta:
        db_table = 'recording'
        get_latest_by = 'date'


class TrendingManager(models.Manager):
    def create_trending(self, rank, title, url, views, channel, handle, record_id):
        channel, create = Channel.objects.get_or_create(name=channel, handle=handle)
        video, create = Video.objects.get_or_create(url=url,
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
    customs = TrendingManager()
    objects = models.Manager()

    class Meta:
        db_table = 'trending'
        ordering = ['rank']
