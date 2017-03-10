# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from datetime import datetime

class SseFundAnnouncementPipeline(object):

    def __init__(self, mysql_host, mysql_user, mysql_password, store_db, store_table, status_db, status_table):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.store_db = store_db
        self.store_table = store_table
        self.status_db = status_db
        self.status_table = status_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            store_db=crawler.settings.get('STORE_DB'),
            store_table=crawler.settings.get('STORE_TABLE'),
            status_db=crawler.settings.get('STATUS_DB'),
            status_table=crawler.settings.get('STATUS_TABLE')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.mysql_host,
                                    db=self.store_db,
                                    user=self.mysql_user,
                                    password=self.mysql_password,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.begin_time = datetime.now()

    def close_spider(self, spider):
        self.conn.commit()
        logging.info('------------------------------------ store data done -------------------------------')
        self.conn.close()
        self.end_time = datetime.now()
        self.store_status(self.begin_time, self.end_time)

    def process_item(self, item, spider):
        with self.conn.cursor() as cursor:
            announ_date = item.get('announ_date')
            stock_code = item.get('stock_code')
            title = item.get('title')
            pdf_url = item.get('pdf_url')
            sql = 'insert into sse_found_announcement (Announ_date, Stock_code, Title, PDF_URL) ' \
                  'values (%s, %s, %s, %s)'
            logging.info('------------------------------print sql-----------------------------------')
            logging.info(sql)
            try:
                cursor.execute(sql, (announ_date, stock_code, title, pdf_url))
                logging.info('--------------------execute sql sucess --------------------------------')
            except Exception as e:
                logging.debug(e)
                self.conn.rollback()
        return item

    def store_status(self, begin_time, end_time):
        status_conn = pymysql.connect(host=self.mysql_host,
                                      user=self.mysql_user,
                                      password=self.mysql_password,
                                      db=self.status_db,
                                      charset='utf8',
                                      cursorclass=pymysql.cursors.DictCursor)
        try:
            with status_conn.cursor() as cur:
                sql = "insert into `program_status` (`name`, `start_time`, `end_time`, `status`) values (%s, %s, %s, %s);"
                cur.execute(sql, ('sse_found_announcement', begin_time, end_time, '1'))
            status_conn.commit()
        finally:
            status_conn.close()
