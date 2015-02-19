import scrapy
from confoo.items import TalkDetailItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import json
from pprint import pprint

class TalkDetailsSpider(scrapy.Spider):
    name = "talk_details"
    allowed_domains = ["confoo.ca"]

    start_urls = []

    def __init__(self):
        json_data=open('talks.json')

        data = json.load(json_data)

        # self.start_urls.append(data[0]['url'][0])
        for entry in data[0]:
            print entry
            self.start_urls.append(entry['url'][0])

        json_data.close()

    def parse(self, response):        
        sel = response.xpath('//div[@class="col-md-9 content"]')
        item = TalkDetailItem()
        item['url'] = response.url
        item['description'] = sel.xpath('div[@class="h-session session-page"]/div/div[@class="e-description"]/text()').extract()
        item['room'] = sel.xpath('div[@class="h-session session-page"]/div[@class="sidebar"]/div[@class="well"]/p/b[@class="p-room"]/text()').extract()
        item['date'] = sel.xpath('div[@class="h-session session-page"]/div[@class="sidebar"]/div[@class="well"]/p/span[@class="dt-date"]/text()').extract()
        item['time'] = sel.xpath('div[@class="h-session session-page"]/div[@class="sidebar"]/div[@class="well"]/p/span[@class="dt-time"]/text()').extract()
        return item
