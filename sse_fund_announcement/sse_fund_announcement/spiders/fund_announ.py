# -*- encoding:utf8 -*-

import scrapy
import logging
import json
from ..items import SseFundAnnouncementItem


class FundSpider(scrapy.Spider):
    name = "sse_fund_announcement"

    def start_requests(self):
        start_url = ('http://query.sse.com.cn/infodisplay/queryBulletinFundNew2.do?'
                     'jsonCallBack=jsonpCallback53702&isPagination=true&productId=&reportType2=&'
                     'reportType=ALL&beginDate={0}-01-01&endDate={0}-12-30'
                     '&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1'
                     '&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1489134164173')

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
                   }
        for year in range(2017, 2018):
            logging.info(year)
            url = start_url.format(year)
            logging.info(url)
            yield scrapy.Request(url=url,
                                 headers=headers,
                                 meta={'year': year, 'headers': headers},
                                 callback=self.generate_link)

    def generate_link(self, response):
        raw_url = ('http://query.sse.com.cn/infodisplay/queryBulletinFundNew2.do?'
                   'jsonCallBack=jsonpCallback53702&isPagination=true&productId=&reportType2=&'
                   'reportType=ALL&beginDate={0}-01-01&endDate={0}-12-30'
                   '&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo={1}'
                   '&pageHelp.beginPage={1}&pageHelp.cacheSize=1&pageHelp.endPage={2}&_=1489134164173')
        raw_data = response.text.split('(')[1].strip(')')
        formated_data = json.loads(raw_data)
        page_count = formated_data['pageHelp']['pageCount']
        year = response.meta['year']
        headers = response.meta['headers']
        for index in range(1, page_count + 1):
            cur_url = raw_url.format(year, index, str(index) + '1')
            yield scrapy.Request(url=cur_url, headers=headers, callback=self.parse)

    def parse(self, response):
        raw_data = response.text
        content = raw_data.split('(')[1].strip(')')
        formated_data = json.loads(content)
        records = formated_data['result']
        base_url = 'http://static.sse.com.cn'
        item = SseFundAnnouncementItem()
        for record in records:
            item['announ_date'] = record['SSEDate']
            item['stock_code'] = record['security_Code']
            item['title'] = record['title']
            item['pdf_url'] = base_url + record['URL']
            yield item
