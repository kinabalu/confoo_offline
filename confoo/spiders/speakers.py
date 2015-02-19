import scrapy
from confoo.items import SpeakerItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import json
from pprint import pprint

class SpeakersSpider(scrapy.Spider):
    name = "speakers"
    allowed_domains = ["confoo.ca"]

    start_urls = []

    def __init__(self):
        json_data=open('talks.json')

        data = json.load(json_data)
        
        # self.start_urls.append(data[0]['speaker_url'][0])
        for entry in data:
            print entry
            self.start_urls.append(entry['speaker_url'][0])

        json_data.close()

    def parse(self, response):
        item = SpeakerItem()
        item['url'] = response.url
        item['name'] = response.xpath('//h1/text()').extract()
        item['bio'] = response.xpath('//div[@class="speaker-page"]/div[@class="speaker"]/p/text()').extract()
        item['speaker_photo'] = response.xpath('//div[@class="speaker-page"]/div[@class="speaker"]/div[@class="media media-frame frame-thin"]/img/@src').extract()
        item['company_url'] = response.xpath('//div[@class="speaker-page"]/div[@class="speaker"]/div[@class="sidebar"]/div[@class="well"]/p/a/@href').extract()
        item['twitter'] = response.xpath('//div[@class="speaker-page"]/div[@class="speaker"]/div[@class="sidebar"]/div[@class="well"]/a[@title="Twitter"]/@href').extract()
        return item

