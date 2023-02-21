from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class YoutubeScrapyPipeline:
    def __init__(self):
        self.ids_set = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['rank'] in self.ids_set:
            raise DropItem(f'중복된 아이템입니다: {item}')
        else:
            self.ids_set.add(adapter['rank'])
            print(item)
            return item

