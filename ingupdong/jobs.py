import os
import time

import requests
from bs4 import BeautifulSoup
from django.db import connections
from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution

from ingupdong.models import RecordingBoard, TrendingBoard


CRAWL_URL = os.environ.get('CRAWL_URL', 'localhost')


def get_num(string):
    new_string = string.replace(",", "")
    return new_string[:-1]


def clear_param(string):
    return string[1:]


@util.close_old_connections
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

    for index, video in enumerate(videos, start=1):
        tags = video.find_all("yt-formatted-string", limit=2)
        TrendingBoard.customs.create_trending(rank=index,
                                              title=tags[0].string,
                                              url=clear_param(tags[0].parent['href']),
                                              views=get_num(tags[0]['aria-label'].split(' ').pop()),
                                              channel_name=tags[1].a.string,
                                              handle=clear_param(tags[1].a['href']),
                                              record_id=record_id,
                                              )


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


@util.close_old_connections
def connect_with_db():
    connections['default'].connect()
