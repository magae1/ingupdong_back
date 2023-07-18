from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import ScoreOnChannel
from ingeupdong.models import Channel
from ingeupdong.signals import after_crawl_trending


@receiver(after_crawl_trending)
def score_on_channel_by_trends(sender, scores, **kwargs):
    for k, v in scores.items():
        score_obj = ScoreOnChannel.objects.get(channel=v[0])
        score_obj.score += (v[1] * 7)
        score_obj.save()


@receiver(post_save, sender=Channel)
def add_score_on_channel(sender, instance, created, **kwargs):
    if created:
        ScoreOnChannel.objects.create(channel=instance)
        