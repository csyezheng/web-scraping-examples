# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CffexPositionRankingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_id = scrapy.Field()
    trade_date = scrapy.Field()
    instrument = scrapy.Field()
    rank_type = scrapy.Field()
    rank = scrapy.Field()
    member_abbrname = scrapy.Field()
    partyid = scrapy.Field()
    volume = scrapy.Field()
    change_volume = scrapy.Field()

