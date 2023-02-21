import scrapy
from .. import items
from bs4 import BeautifulSoup


class YoutubeSpider(scrapy.Spider):
    name = "youtube"
    allowed_domains = ["youtube.com"]

    def start_requests(self):
        url = "https://youtube.com/feed/trending"
        yield scrapy.Request(url=url,
                             callback=self.parse,
                             meta={"playwright": True})

    def parse(self, response):
        videos = response.xpath('//ytd-video-renderer')
        for index, video in enumerate(videos):
            if index == 50:
                break
            soup = BeautifulSoup(video.get(), 'html.parser')
            tags = soup.find_all("yt-formatted-string", limit=2)
            yield self.get_video_item(index+1, tags)

    def get_video_item(self, index, tags):
        item = items.VideoItem()
        item['rank'] = index
        item['title'] = tags[0].string
        item['url'] = self.clear_param(tags[0].parent['href'])
        item['views'] = self.get_num(tags[0]['aria-label'].split(' ').pop())
        item['channel'] = tags[1].a.string
        item['channel_uuid'] = self.clear_param(tags[1].a['href'])
        return item

    def get_num(self, string):
        new_string = string.replace(",", "")
        return new_string[:-1]

    def clear_param(self, string):
        return string[1:]
