import requests
import json
from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution
from ingupdong.models import RecordingBoard, TrendingBoard


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def get_new_trending():
    req = requests.get(url="http://localhost:9080/crawl.json",
                       params={
                           "spider_name": "youtube",
                           "start_requests": "true",
                       },
                       timeout=20)
    res = req.json()['items']
    req.close()
    print(res)


def print_hellos():
    print("Hello World!")
