from django.dispatch import receiver

from .models import ScoringBoard
from ingeupdong.signals import after_crawl_trending


@receiver(after_crawl_trending)
def score_on_channel(sender, trend_objs, **kwargs):
    print(f'Starting {sender}')
    scores = []
    for trend in trend_objs:
        score = (51 - trend.rank) * 5
        scores.append(ScoringBoard(channel=trend.video.channel,
                                   score=score))
    ScoringBoard.objects.bulk_create(scores)
    print(f'Finishing {sender}')
