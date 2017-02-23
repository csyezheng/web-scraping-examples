# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BanstockItem(scrapy.Item):
    rank = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    buy = scrapy.Field()
    sell = scrapy.Field()
    price = scrapy.Field()
    change = scrapy.Field()
