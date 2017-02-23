# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging 
import pymysql

class BanstockPipeline(object):

    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password, mysql_table):
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_table = mysql_table
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host = crawler.settings.get('MYSQL_HOST'),
            mysql_db = crawler.settings.get('MYSQL_DB'),
            mysql_user = crawler.settings.get('MYSQL_USER'),
            mysql_password = crawler.settings.get('MYSQL_PASSWORD'),
            mysql_table = crawler.settings.get('MYSQL_TABLE')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.mysql_host, 
                                    db=self.mysql_db, 
                                    user=self.mysql_user, 
                                    password=self.mysql_password,
                                    charset='utf8', 
                                    cursorclass=pymysql.cursors.DictCursor)
        
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        with self.conn.cursor() as cursor:
            rank = item['rank']
            code = item['code']
            name = item['name']
            buy = item['buy']
            sell = item['sell']
            price = item['price']
            change = item['change']
            sql = 'insert into banstock (Rank, Code, Name, Buy, Sell, Price, `Change`) values ({0},"{1}","{2}",{3},{3},{5},{6});'.format(rank,code,name,buy,sell,price,change)
            try:
                logging.info(name)
                logging.info(sql)
                cursor.execute(sql,())
                logging.info('execute sucess')
            except Exception as e:
                print(e)
                self.conn.rollback()
        return item



