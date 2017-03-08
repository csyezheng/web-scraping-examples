# -*- encoding: utf-8 -*-

import scrapy
import logging
import json
from ..items import BasicInfoItem, CapitalItem, TopTenMapItem, BalanceItem, ProfitItem, CashItem

class ListXBRL(scrapy.Spider):
    """scraping http://listxbrl.sse.com.cn/ """

    name = "sse_listxbrl"

    def start_requests(self):
        start_urls = ['http://listxbrl.sse.com.cn/report/list.do']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.real_requests)

    def real_requests(self, response):
        formated_data = json.loads(response.text)
        reports = formated_data['rows']
        for report in reports:
            stock_id = report['stock_id']
            report_year = report['report_year']
            report_period_id = report['report_period_id']
            form_data = {'stock_id': stock_id, 'report_year': report_year, 'report_period_id': report_period_id}
            urls = ['http://listxbrl.sse.com.cn/companyInfo/showmap.do',
                    'http://listxbrl.sse.com.cn/capital/showmap.do'
                    'http://listxbrl.sse.com.cn/companyInfo/showTopTenMap.do',
                    'http://listxbrl.sse.com.cn/companyInfo/showBalance.do',
                    'http://listxbrl.sse.com.cn/profit/showmap.do',
                    'http://listxbrl.sse.com.cn/cash/showmap.do']
            for url in urls:
                yield scrapy.FormRequest(url=url,
                                         formdata=form_data,
                                         meta={'stock_id': stock_id},
                                         callback=self.distribute)

    def distribute(self, response):
        url = response.url
        if 'capital' in url:
            self.capital_parse(response)
        elif 'showTopTenMap' in url:
            self.top_ten_map_parse(response)
        elif 'showBalance' in url:
            self.balance_parse(response)
        elif 'profit' in url:
            self.profit_parse(response)
        elif 'cash' in url:
            self.cash_parse(response)
        else:
            self.basic_info_parse(response)

    def basic_info_parse(self, response):
        formated_data = json.loads(response.text)
        records = formated_data['rows']
        item = BasicInfoItem()
        for record in records:
            item['y2016'] = self.extract(record['value0'])
            item['y2015'] = self.extract(record['value1'])
            item['y2014'] = self.extract(record['value2'])
            item['y2013'] = self.extract(record['value3'])
            item['y2012'] = self.extract(record['value4'])
            yield item


    def capital_parse(self, response):
        formated_data = json.loads(response.text)
        records = formated_data['rows']
        item = CapitalItem()
        for record in records:
            item['y2016'] = record['value0']
            item['y2015'] = record['value1']
            item['y2014'] = record['value2']
            item['y2013'] = record['value3']
            item['y2012'] = record['value4']
            yield item

    def top_ten_map_parse(self, response):
        formated_data = json.loads(response.text)
        records = formated_data['rows']
        item = TopTenMapItem()
        for record in records:
            item['y2016'] = self.extract(record['value0'])
            item['y2015'] = self.extract(record['value1'])
            item['y2014'] = self.extract(record['value2'])
            item['y2013'] = self.extract(record['value3'])
            item['y2012'] = self.extract(record['value4'])
            yield item

    def balance_parse(self, response):
        formated_data = json.loads(response.text)
        records = formated_data['rows']
        item = BalanceItem()
        for record in records:
            item['y2016'] = record['value0']
            item['y2015'] = record['value1']
            item['y2014'] = record['value2']
            item['y2013'] = record['value3']
            item['y2012'] = record['value4']
            yield item

    def profit_parse(self, response):
        formated_data = json.loads(response.text)
        records = formated_data['rows']
        item = ProfitItem()
        for record in records:
            item['y2016'] = record['value0']
            item['y2015'] = record['value1']
            item['y2014'] = record['value2']
            item['y2013'] = record['value3']
            item['y2012'] = record['value4']
            yield item

    def cash_parse(self, response):
        formated_data = json.loads(response.text)
        records = formated_data['rows']
        item = CashItem()
        for record in records:
            item['y2016'] = record['value0']
            item['y2015'] = record['value1']
            item['y2014'] = record['value2']
            item['y2013'] = record['value3']
            item['y2012'] = record['value4']
            yield item

    def extract(self, elem):
        if '<' in elem and '>' in elem:
            elem = elem.split('>')[1].split('<')[0]
        return elem.replace('</br>', '\n')




