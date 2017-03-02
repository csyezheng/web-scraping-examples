# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CapitalFlowsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    super_in = scrapy.Field()
    super_out = scrapy.Field()
    big_in = scrapy.Field()
    big_out = scrapy.Field()
    middle_in = scrapy.Field()
    middle_out = scrapy.Field()
    small_in = scrapy.Field()
    small_out = scrapy.Field()
    trade_date = scrapy.Field()
