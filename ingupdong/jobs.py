import os
import requests
from django_apscheduler import util
from ingupdong.models import RecordingBoard, TrendingBoard


SCRAPY_URL = os.environ.get('SCRAPY_URL', 'localhost')


@util.close_old_connections
@util.retry_on_db_operational_error
def get_new_trending():
    record_id = RecordingBoard.objects.create().id
    req = requests.get(url=f'http://{SCRAPY_URL}:9080/crawl.json',
                       params={
                           "spider_name": "youtube",
                           "start_requests": "true",
                       },
                       timeout=100)
    req.close()
    items = req.json()['items']
    for item in items:
        TrendingBoard.customs.create_trending(rank=item['rank'],
                                              title=item['title'],
                                              url=item['url'],
                                              views=item['views'],
                                              channel=item['channel'],
                                              handle=item['handle'],
                                              record_id=record_id,
                                              )


def print_hellos():
    print("Hello World!")
