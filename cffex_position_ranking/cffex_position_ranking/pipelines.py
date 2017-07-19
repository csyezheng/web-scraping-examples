# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymysql
import logging


class CffexPositionRankingPipeline(object):
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
        self.begin_time = datetime.datetime.now()
        self.conn = pymysql.connect(host=self.mysql_host,
                                    user=self.mysql_user,
                                    password=self.mysql_password,
                                    db=self.store_db,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        product_id = item['product_id']
        trade_date = item['trade_date']
        instrument = item['instrument']
        rank_type = item['rank_type']
        rank = item['rank']
        member_abbrname = item['member_abbrname']
        partyid = item['partyid']
        volume = item['volume']
        change_volume = item['change_volume']
        now = datetime.datetime.now()
        sql = ('insert into {0} (`product_id`, `trade_date`, `instrument`, `rank_type`, `rank`, `member_abbrname`, '
               '`partyid`, `volume`, `change_volume`, `crawl_time`) '
               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)').format(self.store_table)
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (product_id, trade_date, instrument, rank_type, rank, member_abbrname, partyid,
                                  volume, change_volume, now))
                logging.info('-----------------execute inserting operation success ----------------------')
        except Exception as e:
            logging.info('----------------------- insert failed -------------------------')
            logging.debug(e)
        return item

    def close_spider(self, spider):
        try:
            self.conn.commit()
            logging.info('--------------------- commit success -------------------')
            self.end_time = datetime.datetime.now()
            self.store_status(self.begin_time, self.end_time)
        except Exception as e:
            logging.debug(e)
        finally:
            self.conn.close()


    def store_status(self, begin_time, end_time):
        status_conn = pymysql.connect(host=self.mysql_host,
                                      user=self.mysql_user,
                                      password=self.mysql_password,
                                      db=self.status_db,
                                      charset='utf8',
                                      cursorclass=pymysql.cursors.DictCursor)
        try:
            with status_conn.cursor() as cur:
                sql = "insert into `{0}` (`name`, `start_time`, `end_time`, `status`) " \
                      "values (%s, %s, %s, %s);".format(self.status_table)
                cur.execute(sql, ('cffex_position_ranking', begin_time, end_time, '1'))
            status_conn.commit()

        finally:
            status_conn.close()