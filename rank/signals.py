from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import ScoreOnChannel
from ingeupdong.models import Channel, Video
from ingeupdong.signals import after_crawl_trending


def score_by_datedelta(target, offset=datetime.today(), max_score=100):
    timedelta = offset - target
    return min(timedelta.days, max_score)
    

@receiver(after_crawl_trending)
def score_on_channel_by_trends(sender, scores, **kwargs):
    for k, v in scores.items():
        score_obj = ScoreOnChannel.objects.get(channel=v[0])
        
        try:
            before_latest_video_obj = Video.objects.filter(channel=v[0]).order_by('-created_at')[1]
            added_score = score_by_datedelta(before_latest_video_obj.created_at)
        except IndexError as e:
            added_score = 50
        score_obj.score += (v[1] * 2) + added_score
        score_obj.save()


@receiver(post_save, sender=Channel)
def add_score_on_channel(sender, instance, created, **kwargs):
    if created:
        ScoreOnChannel.objects.create(channel=instance, score=100)
        