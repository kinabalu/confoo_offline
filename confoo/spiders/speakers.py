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
        
        # self.start_urls.append(data[2]['speaker_url'][0])
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
        item['talks'] = response.xpath('//div[@class="session-list"]/h3/a/@href').extract()

        return item

"""
<div class="session-list">

    <h2>2015 sessions</h2>


    <h3>
        <a href="http://confoo.ca/en/2015/session/an-introduction-to-amazon-web-services" title="View session page">
            An Introduction to Amazon Web Services<span class="glyphicon glyphicon-link"></span>
        </a>
    </h3>

    <p>English session                  - Beginner          </p>

    <p>Haven't got time to learn all about nodes and clouds and elastics? This introductory session will give you a baseline for getting started on AWS.<br>
<br>
In this talk, we'll cover file hosting (S3), server hosting (EC2, VPC), DNS hosting (Route53), database hosting (RDS), and some additional things like Cloudwatch, CloudFront, and ElasticCache, but we'll focus on the moving parts of EC2.</p>


    <h3>
        <a href="http://confoo.ca/en/2015/session/inspect-http-s-with-your-own-man-in-the-middle-non-attacks" title="View session page">
            Inspect HTTP(S) with Your Own Man-in-the-Middle Non-Attacks<span class="glyphicon glyphicon-link"></span>
        </a>
    </h3>

    <p>English session                  - Advanced          </p>

    <p>Aren't sure your mobile app will play nice with your next web app release? Got a tricky session-related bug that's difficult to reproduce in the browser, but is confounding your support team? Just want to see what your HTML pages are loading, and when? Sounds like a job for an inspecting proxy server like Charles or mitmproxy!<br>
<br>
We'll cover inspecting HTTP(S) proxy basic, &amp; some use cases for why and when this skillset should be in your toolkit.</p>

"""
