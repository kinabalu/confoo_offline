# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TalkItem(scrapy.Item):
    session_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    speaker_thumb = scrapy.Field()
    speaker_name = scrapy.Field()
    speaker_url = scrapy.Field()

class TalkDetailItem(scrapy.Item):
    url = scrapy.Field()
    description = scrapy.Field()
    room = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()

class SpeakerItem(scrapy.Item):
    url = scrapy.Field()
    bio = scrapy.Field()
    name = scrapy.Field()
    speaker_photo = scrapy.Field()
    twitter = scrapy.Field()
    company_url = scrapy.Field()
    talks = scrapy.Field()
