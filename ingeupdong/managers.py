from django.db import models


class RecordingManager(models.Manager):
    def get_by_datetime(self, date):
        return self.filter(record_at__day=date.day,
                           record_at__month=date.month,
                           record_at__year=date.year,
                           record_at__hour=date.hour).last()


class TrendingManager(models.Manager):
    def counts_of_period_days(self, channel_obj, prev_date):
        recent_records_obj = self.filter(record__record_at__gt=prev_date, video__channel=channel_obj)
        recent_records_obj = recent_records_obj.values('record__record_at__date')
        recent_records_obj = recent_records_obj.order_by('record__record_at__date')
        recent_records_obj = recent_records_obj.annotate(count=models.Count('video_id', distinct=True))
        return recent_records_obj.values('record__record_at__date', 'count')
    
    