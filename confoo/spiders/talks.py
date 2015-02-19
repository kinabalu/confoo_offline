import scrapy
from confoo.items import TalkItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class ConfooSpider(scrapy.Spider):
    name = "talks"
    allowed_domains = ["confoo.ca"]

    start_urls = [
        "http://confoo.ca/en/2015/sessions"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="session-list row"]/div[@class="col-md-6"]'):
            item = TalkItem()
            item['title'] = sel.xpath('div[@class="h-session session"]/a[@class="p-title u-url"]/text()').extract()
            item['url'] = sel.xpath('div[@class="h-session session"]/a[@class="p-title u-url"]/@href').extract()
            item['session_id'] = sel.xpath('div[@class="h-session session"]/@id').extract()
            item['speaker_thumb'] = sel.xpath('div[@class="h-session session"]/img[@class="photo"]/@src').extract()
            item['speaker_name'] = sel.xpath('div[@class="h-session session"]/div/a[@class="p-speaker"]/text()').extract()
            item['speaker_url'] = sel.xpath('div[@class="h-session session"]/div/a[@class="p-speaker"]/@href').extract()
            yield item

"""
<div class="col-md-6"><div class="h-session session" id="session_1618">
        <img class="photo" src="/images/speakers/2015/mario-cardinal_s.jpg">
        <a href="http://confoo.ca/en/2015/session/a-personal-perspective-on-architecting-mobile-applications" class="p-title u-url">A Personal Perspective on Architecting Mobile Applications</a>
        <a data-session="1618" href="/en/wishlist/1618" class="btn-fave" title="Wish List" style="display: none; cursor: pointer;"><span class="glyphicon"></span></a>
        <div>
    <a href="http://confoo.ca/en/speaker/mario-cardinal" class="p-speaker">Mario Cardinal</a><br><span class="tag architecture {'id':'architecture'}">Architecture</span><span class="tag mobile {'id':'mobile'}">Mobile</span></div></div></div>
"""
