# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging
from .items import BasicInfoItem, CapitalItem, TopTenMapItem, BalanceItem, ProfitItem, CashItem


class SseListxbrlPipeline(object):
    def __init__(self, store_host, store_user, store_password, store_db, sse_basic_info,
                 sse_capital, sse_top_ten_map, sse_balance, sse_profit, sse_cash):
        self.store_host = store_user
        self.store_user = store_user
        self.store_password = store_password
        self.store_db = store_db
        self.sse_basic_info = sse_basic_info
        self.sse_capital = sse_capital
        self.sse_capital = sse_capital
        self.sse_top_ten_map = sse_top_ten_map
        self.sse_balance = sse_balance
        self.sse_profit = sse_profit
        self.sse_case = sse_cash

    @classmethod
    def from_crawler(cls, crawler):
        return cls(store_host = crawler.settings.get('STORE_HOST'),
                   store_user = crawler.settings.get('STORE_USER'),
                   store_password = crawler.settings.get('STORE_PASSWORD'),
                   store_db = crawler.settings.get('STORE_DB'),
                   sse_basic_info = crawler.settings.get('SSE_BASIC_INFO'),
                   sse_capital = crawler.settings.get('SSE_CAPITAL'),
                   sse_top_ten_map = crawler.settings.get('SSE_TOP_TEN_MAP'),
                   sse_balance = crawler.settings.get('SSE_BALANCE'),
                   sse_profit = crawler.settings.get('SSE_PROFIT'),
                   sse_cash = crawler.settings.get('SSE_CASH'))

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.store_host,
                                    user=self.store_user,
                                    password=self.store_password,
                                    db=self.store_db,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)


    def process_item(self, item, spider):
        value_2016 = item.get('y2016')
        value_2015 = item.get('y2015')
        value_2014 = item.get('y2014')
        value_2013 = item.get('y2013')
        value_2012 = item.get('y2012')
        if isinstance(item, BasicInfoItem):
            table = 'sse_basic_info'
        elif isinstance(item, CapitalItem):
            table = 'sse_capital'
        elif isinstance(item, TopTenMapItem):
            table = 'sse_top_ten_map'
        elif isinstance(item, BalanceItem):
            table = 'sse_balance'
        elif isinstance(item, ProfitItem):
            table = 'sse_profit'
        elif isinstance(item, CashItem):
            table = 'sse_cash'
        sql = ('inser into `{0}` (`Y2016`, `Y2015`, `Y2014`, `Y2013`, `Y2012`) '
              'values (%s, %s, %s, %s, %s)').format(table)
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (value_2016, value_2015, value_2014, value_2013, value_2012))
        except:
            logging.info('error occur')

        return item
