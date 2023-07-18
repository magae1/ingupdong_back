from django.db import models

from ingeupdong.models import Channel


class ScoreOnChannel(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='score')
    score = models.IntegerField(default=0, null=False)
    
    class Meta:
        db_table = 'score_on_channel'
        ordering = ['-score']
    
    def __str__(self):
        return f'[{self.channel_id}]{self.channel.name}: {self.score}'
    