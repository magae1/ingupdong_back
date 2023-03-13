import os
import requests
from bs4 import BeautifulSoup
from django_apscheduler import util
from django.db import connection
from django.db.utils import OperationalError
from ingupdong.models import RecordingBoard, TrendingBoard


CRAWL_URL = os.environ.get('CRAWL_URL', 'localhost')


def get_num(string):
    new_string = string.replace(",", "")
    return new_string[:-1]


def clear_param(string):
    return string[1:]


@util.close_old_connections
@util.retry_on_db_operational_error
def crawl_youtube_trending():
    req = requests.get(url=f'https://{CRAWL_URL}/crawl-youtube-by-selenium', timeout=30)
    soup = BeautifulSoup(req.text, 'html.parser')
    req.close()
    record_id = RecordingBoard.objects.create().id

    video_sections = soup.find_all('ytd-expanded-shelf-contents-renderer')
    videos = video_sections[0].find_all('ytd-video-renderer') + video_sections[1].find_all('ytd-video-renderer')

    for index, video in enumerate(videos):
        tags = video.find_all("yt-formatted-string", limit=2)
        TrendingBoard.customs.create_trending(rank=index+1,
                                              title=tags[0].string,
                                              url=clear_param(tags[0].parent['href']),
                                              views=get_num(tags[0]['aria-label'].split(' ').pop()),
                                              channel=tags[1].a.string,
                                              handle=clear_param(tags[1].a['href']),
                                              record_id=record_id,
                                              )


def print_hellos():
    print("Hello World!")
