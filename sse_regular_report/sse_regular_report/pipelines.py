# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging


class SseRegularReportPipeline(object):
    def __init__(self, store_host, store_user, store_password, store_db, store_table):
        self.store_host = store_host
        self.store_user = store_user
        self.store_password = store_password
        self.store_db = store_db
        self.store_table = store_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(store_host=crawler.settings.get('STORE_HOST'),
                   store_user=crawler.settings.get('STORE_USER'),
                   store_password=crawler.settings.get('STORE_PASSWORD'),
                   store_db=crawler.settings.get('STORE_DB'),
                   store_table=crawler.settings.get('STORE_TABLE'))

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.store_host,
                                    user=self.store_user,
                                    password=self.store_password,
                                    db=self.store_db,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        with self.conn.cursor() as cur:
            announ_date = item['announ_date']
            stock_code = item['stock_code']
            title = item['title']
            pdf_url = item['pdf_url']
            sql = 'insert into `{0}` (`Announ_date`, `Stock_code`, `Title`, `PDF_URL`) values (%s, %s, %s, %s)'.format(
                self.store_table)
            try:
                logging.info(sql)
                cur.execute(sql, (announ_date, stock_code, title, pdf_url))
                logging.info('---------------------------- execute seccuess -------------------------')
            except Exception as e:
                logging.debug(e)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
