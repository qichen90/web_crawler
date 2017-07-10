# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# define extracted Data Schema
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    appid = scrapy.Field()
    intro = scrapy.Field()
    recommened = scrapy.Field()
    thumbnail = scrapy.Field()
    pass
