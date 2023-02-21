import scrapy


class VideoItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()          # 영상 제목
    url = scrapy.Field()
    views = scrapy.Field()
    channel = scrapy.Field()        # 채널명
    channel_uuid = scrapy.Field()
