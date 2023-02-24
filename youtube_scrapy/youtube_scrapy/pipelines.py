import os
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from ingupdong.models import TrendingBoard


class YoutubeScrapyPipeline:
    def __init__(self):
        self.ids_set = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['rank'] in self.ids_set:
            raise DropItem(f'중복된 아이템입니다: {item}')
        self.ids_set.add(adapter['rank'])
        # print(item)
        TrendingBoard.customs.create_trending(rank=adapter['rank'],
                                              title=adapter['title'],
                                              url=adapter['url'],
                                              views=adapter['views'],
                                              channel=adapter['channel'],
                                              handle=adapter['handle'],
                                              record_id=adapter['record_id']
                                              )
        return item

    def open_spider(self, spider):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    def close_spider(self, spider):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "false"
