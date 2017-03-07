# -*- encoding:utf8 -*-

import scrapy
import logging
import json
from ..items import SseListingAnnouncementItem


class ListingAnnounSpider(scrapy.Spider):
    "scraping sse.com.cn issue listing announcement"

    name = "sse_listing_announcement"

    def start_requests(self):
        start_url = ('http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?'
                     'jsonCallBack=jsonpCallback61833&isPagination=true&productId=&keyWord='
                     '&reportType2=LSGG&reportType=FXSSGG&beginDate={0}-01-01&endDate={1}-12-30'
                     '&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1'
                     '&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1488868656873'
                     )

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
                   }

        for year in range(2012, 2018):
            logging.info(year)
            url = start_url.format(year, year)
            logging.info(url)
            yield scrapy.Request(url=url,
                                 headers=headers,
                                 meta={'year': year, 'headers': headers},
                                 callback=self.generate_link)

    def generate_link(self, response):
        raw_url = ('http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?'
                   'jsonCallBack=jsonpCallback61833&isPagination=true&productId=&keyWord='
                   '&reportType2=LSGG&reportType=FXSSGG&beginDate={0}-01-01&endDate={1}-12-30'
                   '&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo={2}'
                   '&pageHelp.beginPage={3}&pageHelp.cacheSize=1&pageHelp.endPage={4}&_=1488868656873'
                   )
        raw_data = response.text.split('(')[1].strip(')')
        formated_data = json.loads(raw_data)
        page_count = formated_data['pageHelp']['pageCount']
        year = response.meta['year']
        headers = response.meta['headers']
        for index in range(1, page_count + 1):
            cur_url = raw_url.format(year, year, index, index, str(index) + '1')
            yield scrapy.Request(url=cur_url, headers=headers, callback=self.parse)

    def parse(self, response):
        raw_data = response.text
        content = raw_data.split('(')[1].strip(')')
        formated_data = json.loads(content)
        records = formated_data['result']
        base_url = 'http://static.sse.com.cn'
        item = SseListingAnnouncementItem()
        for record in records:
            item['announ_date'] = record['SSEDate']
            item['stock_code'] = record['security_Code']
            item['title'] = record['title']
            item['pdf_url'] = base_url + record['URL']
            yield item
