from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from ingupdong.jobs import crawl_youtube_trending, delete_old_job_executions, connect_with_db


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        crawl_youtube_trending,
        trigger=CronTrigger(hour="6,18", minute="00"),
        id="crawl-youtube-trending",
        max_instances=1,
        replace_existing=True,
    )

    scheduler.add_job(
        connect_with_db,
        trigger=CronTrigger(hour="5,17", minute="58", jitter=30),
        id="connect_with_db",
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

