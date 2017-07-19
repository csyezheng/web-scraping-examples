#!/usr/bin/env python3
#-*- encoding:utf-8 -*-

import scrapy
import pymysql
from ..items import CapitalFlowsItem

class CapitalSpider(scrapy.Spider):
    name = 'capital_flows'

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        conn = pymysql.connect(host='192.168.31.181',
                               user='ope1',
                               password='Siteope',
                               db='stock',
                               charset='utf8',
                               cursorclass = pymysql.cursors.DictCursor)
        self.stocks = []
        with conn.cursor() as cur:
            try:
                sql = 'select stock_code from code_stocka_wind'
                cur.execute(sql, ())
                records = cur.fetchall()
                for record in records:
                    stock, sign = record['stock_code'].split('.')
                    sign = '1' if sign == 'SH' else '2'
                    stock += sign
                    self.stocks.append(stock)
            finally:
                conn.close()

    def start_requests(self):
        for stock in self.stocks:
            data = 'data:[x]'
            url = ('http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?'
                   'type=CT&cmd={0}&sty=CTBFTA&st=z&sr=&p=&ps=&cb=&js=var%20tab_data=({1})'
                   '&token=70f12f2f4f091e459a279469fe49eca5').format(stock, data)
            headers = {'Referer': 'http://data.eastmoney.com/zjlx/',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Ubuntu Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36'}
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        self.logger.info('-------------------------- start parse ----------------------------------------------')
        raw_data = response.xpath('//body//p//text()').extract_first().split('"')[1]
        data_lst = raw_data.split(',')
        item = CapitalFlowsItem()
        item['stock_code'] = data_lst[1]
        item['super_in'] = data_lst[8]
        item['super_out'] = data_lst[9]
        item['big_in'] = data_lst[12]
        item['big_out'] = data_lst[13]
        item['middle_in'] = data_lst[15]
        item['middle_out'] = data_lst[16]
        item['small_in'] = data_lst[19]
        item['small_out'] = data_lst[20]
        item['trade_date'] = data_lst[24]
        return item
