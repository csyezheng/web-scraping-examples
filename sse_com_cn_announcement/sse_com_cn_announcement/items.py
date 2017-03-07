# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SseComCnAnnouncementItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    announ_date = scrapy.Field()
    stock_code = scrapy.Field()
    title = scrapy.Field()
    pdf_url = scrapy.Field()
