import requests
from bs4 import BeautifulSoup
from django.db import connections, transaction, OperationalError
from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution

from ingeupdong.models import RecordingBoard, Video, TrendingBoard, Channel
from ingeupdong.signals import after_crawl_trending
from rank.jobs import discount_scores
from config.settings import CRAWL_URL
from .utils import clear_param, get_num


@util.retry_on_db_operational_error
def crawl_youtube_trending():
    videos = []
    while True:
        req = requests.get(url=f'https://{CRAWL_URL}/crawl-youtube-by-selenium', timeout=30)
        soup = BeautifulSoup(req.text, 'html.parser')
        req.close()
        record_id = RecordingBoard.objects.create().id

        try:
            video_sections = soup.find_all('ytd-expanded-shelf-contents-renderer')
            videos = video_sections[0].find_all('ytd-video-renderer') + video_sections[1].find_all('ytd-video-renderer')
        except IndexError:
            continue
        else:
            break
    
    scores = {}
    trend_objs = []
    for index, video in enumerate(videos, start=1):
        tags = video.find_all("yt-formatted-string", limit=2)
        with transaction.atomic():
            channel_obj, created = Channel.objects.update_or_create(handle=clear_param(tags[1].a['href']),
                                                                    defaults={'name': tags[1].a.string})
            video_obj, created = Video.objects.update_or_create(channel=channel_obj,
                                                                url=clear_param(tags[0].parent['href']),
                                                                defaults={'title': tags[0].string})
            
        trend_objs.append(TrendingBoard(rank=index,
                                        video=video_obj,
                                        views=get_num(tags[0]['aria-label'].split(' ').pop()),
                                        record_id=record_id))
        index = (len(videos) + 1) - index
        if channel_obj.id in scores:
            scores[channel_obj.id] = (channel_obj, scores[channel_obj.id][1] + index)
        else:
            scores[channel_obj.id] = (channel_obj, index)
            
    TrendingBoard.objects.bulk_create(trend_objs)
    after_crawl_trending.send(sender="crawl_youtube_trend", scores=scores)
    
    
# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
@util.retry_on_db_operational_error
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


@util.retry_on_db_operational_error
def connect_with_db():
    try:
        connections['default'].connect()
    except OperationalError as operational_err:
        print(operational_err)
    discount_scores()
