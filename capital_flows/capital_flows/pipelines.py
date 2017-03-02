# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import pymysql
from datetime import datetime

class CapitalFlowsPipeline(object):
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
        """
        return cls(
            mysql_host='192.168.31.181',
            store_db='test',
            mysql_user='ope1',
            mysql_password='Siteope',
            store_table='eastmoney_zjlx'
        )
        """

    def clear_data(self):
        """store data into database"""

        conn = pymysql.connect(host=self.mysql_host,
                               user=self.mysql_user,
                               password=self.mysql_password,
                               db=self.store_db,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as cur:
                insert_sql = 'delete from `{0}'.format(self.store_table)
                cur.execute(insert_sql, ())
            conn.commit()
        finally:
            conn.close()



    def open_spider(self, spider):
        self.clear_data()
        self.conn = pymysql.connect(host=self.mysql_host,
                                    db=self.store_db,
                                    user=self.mysql_user,
                                    password=self.mysql_password,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        with self.conn.cursor() as cur:
            insert_sql = 'delete from `{0}'.format(self.store_table)
            cur.execute(insert_sql, ())
        self.conn.commit()
        self.begin_time = datetime.now()





    def close_spider(self, spider):
        self.conn.commit()
        logging.info('------------------------------------ store data done -------------------------------')
        self.conn.close()
        self.end_time = datetime.now()
        self.store_status(self.begin_time, self.end_time)




    def process_item(self, item, spider):
        with self.conn.cursor() as cursor:
            stock_code = item.get('stock_code')
            super_in = item.get('super_in')
            super_out = item.get('super_out')
            big_in = item.get('big_in')
            big_out = item.get('big_out')
            middle_in = item.get('middle_in')
            middle_out = item.get('middle_out')
            small_in = item.get('small_in')
            small_out = item.get('small_out')
            trade_date = item.get('trade_date')
            sql = 'insert into eastmoney_zjlx (trade_date, stock_code, super_in, super_out, big_in, big_out, ' \
                  'middle_in, middle_out, small_in, small_out) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            logging.info('------------------------------print sql-----------------------------------')
            logging.info(sql)
            try:
                cursor.execute(sql, (trade_date, stock_code, super_in, super_out, big_in, big_out, middle_in,
                                     middle_out, small_in, small_out))
                logging.info('--------------------execute sql sucess --------------------------------')
            except Exception as e:
                print(e)
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
                cur.execute(sql, ('eastmoney_zjlx', begin_time, end_time, '1'))
            status_conn.commit()
        
        finally:
            status_conn.close()
