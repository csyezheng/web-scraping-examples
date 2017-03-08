# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BasicInfoItem(scrapy.Item):
    stock_id = scrapy.Field()
    y2016 = scrapy.Field()
    y2015 = scrapy.Field()
    y2014 = scrapy.Field()
    y2013 = scrapy.Field()
    y2012 = scrapy.Field()


class CapitalItem(scrapy.Item):
    stock_id = scrapy.Field()
    y2016 = scrapy.Field()
    y2015 = scrapy.Field()
    y2014 = scrapy.Field()
    y2013 = scrapy.Field()
    y2012 = scrapy.Field()

class TopTenMapItem(scrapy.Item):
    stock_id = scrapy.Field()
    y2016 = scrapy.Field()
    y2015 = scrapy.Field()
    y2014 = scrapy.Field()
    y2013 = scrapy.Field()
    y2012 = scrapy.Field()

class BalanceItem(scrapy.Item):
    stock_id = scrapy.Field()
    y2016 = scrapy.Field()
    y2015 = scrapy.Field()
    y2014 = scrapy.Field()
    y2013 = scrapy.Field()
    y2012 = scrapy.Field()

class ProfitItem(scrapy.Item):
    stock_id = scrapy.Field()
    y2016 = scrapy.Field()
    y2015 = scrapy.Field()
    y2014 = scrapy.Field()
    y2013 = scrapy.Field()
    y2012 = scrapy.Field()

class CashItem(scrapy.Item):
    stock_id = scrapy.Field()
    y2016 = scrapy.Field()
    y2015 = scrapy.Field()
    y2014 = scrapy.Field()
    y2013 = scrapy.Field()
    y2012 = scrapy.Field()