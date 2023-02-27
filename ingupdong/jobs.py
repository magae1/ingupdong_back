import requests
from django_apscheduler import util
from ingupdong.models import RecordingBoard, TrendingBoard


@util.close_old_connections
def get_new_trending():
    record_id = RecordingBoard.objects.create().id
    req = requests.get(url="http://localhost:9080/crawl.json",
                       params={
                           "spider_name": "youtube",
                           "start_requests": "true",
                       },
                       timeout=25)
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
    req.close()


def print_hellos():
    print("Hello World!")
