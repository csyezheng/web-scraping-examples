# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging


class SseMaginAnnouncementPipeline(object):
    def __init__(self, store_host, store_user, store_password, store_db):
        self.store_host = store_host
        self.store_user = store_user
        self.store_password = store_password
        self.store_db = store_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            store_host = crawler.settings.get('STORE_HOST'),
            store_user = crawler.settings.get('STORE_USER'),
            store_password = crawler.settings.get('STORE_PASSWORD'),
            store_db = crawler.settings.get('STORE_DB')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.store_host,
                                    user=self.store_user,
                                    password=self.store_password,
                                    db=self.store_db,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)


    def process_item(self, item, spider):
        logging.info('======================== begin process item ==================================')
        title = item.get('title')
        announ_date = item.get('announ_date')
        content = item.get('content')
        with self.conn.cursor() as cur:
            sql = "insert into `sse_magin_announcement` (`Title`, `Announ_date`, `Content`) values (%s, %s, %s);"
            cur.execute(sql, (title, announ_date, content))
        return item


    def close_spider(self, spider):
        try:
            self.conn.commit()
        except:
            logging.debug('error occur on commiting database')
        finally:
            self.conn.close()
