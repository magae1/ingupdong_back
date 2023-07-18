from ingeupdong.models import Channel
from .models import ScoreOnChannel


def discount_scores():
    score_objs = ScoreOnChannel.objects.all()
    for obj in score_objs:
        obj.score = obj.score // 10
    ScoreOnChannel.objects.bulk_update(score_objs, ['score'])
    