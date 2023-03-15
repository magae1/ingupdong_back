from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from ingupdong.jobs import crawl_youtube_trending, delete_old_job_executions


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(
        crawl_youtube_trending,
        trigger=CronTrigger(hour="21"),
        id="crawl-youtube-trending",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )

    scheduler.start()

