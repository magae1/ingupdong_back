from django.dispatch import receiver

from .models import ScoringBoard
from ingeupdong.signals import after_crawl_trending


@receiver(after_crawl_trending)
def score_on_channel_by_trends(sender, trend_objs, **kwargs):
    print(f'Starting {sender}')
    scores = {}
    for trend in trend_objs:
        score = (51 - trend.rank) * 10
        if trend.video.channel_id in scores:
            scores[trend.video.channel_id] = (trend.video.channel, scores[trend.video.channel_id][1] + score)
        else:
            scores[trend.video.channel_id] = (trend.video.channel, score)
    scores_list = [ScoringBoard(channel=s[0], score=s[1]) for k, s in scores.items()]
    ScoringBoard.objects.bulk_create(scores_list)
    print(f'Finishing {sender}')
