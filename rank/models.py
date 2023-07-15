from datetime import datetime, timedelta

from django.db import models
from ingeupdong.models import Channel


class ScoringBoardManager(models.Manager):
    def delete_old_scores(self, period_days=10):
        target_date = datetime.now() - timedelta(days=period_days)
        self.filter(created_at__lt=target_date).delete()


class ScoringBoard(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'scores_on_channel'
    
    def __str__(self):
        return f'[{self.created_at.strftime("%y/%m/%d %H:%M")}] {self.score} at {self.channel.name}'
    