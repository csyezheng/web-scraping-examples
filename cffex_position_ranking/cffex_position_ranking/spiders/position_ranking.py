#-*- coding: utf8 -*-


import scrapy
import datetime
from ..items import CffexPositionRankingItem


class PositionRankSpider(scrapy.Spider):

    name = 'cffex_position_ranking'

    def __daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):             # + 1 means include end_date
            yield start_date + datetime.timedelta(n)

    def start_requests(self):
        product_types = ['IC', 'IF', 'IH', 'T', 'TF']
        origin_url = 'http://www.cffex.com.cn/fzjy/ccpm/{0}/{1}/{2}.xml'

        begin_date = datetime.datetime.strptime(self.begin_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()

        for search_date in self.__daterange(begin_date, end_date):
            search_date = search_date.strftime('%Y%m%d')
            search_year_month = search_date[0:6]
            search_day = search_date[6:]
            headers = {'Referer': 'http://www.cffex.com.cn/fzjy/ccpm/',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                                     'Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36'}
            for product_type in product_types:
                url = origin_url.format(search_year_month, search_day, product_type)
                yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        records = response.xpath('//data')
        rank_type = ['成交量排名', '持买单量排名', '持卖单量排名']
        for record in records:
            item = CffexPositionRankingItem()
            item['product_id'] = record.xpath('productid/text()').extract_first().strip()
            item['trade_date'] = record.xpath('tradingDay/text()').extract_first()
            item['instrument'] = record.xpath('instrumentId/text()').extract_first().strip()
            type_id = record.xpath('dataTypeId/text()').extract_first()
            item['rank_type'] = rank_type[int(type_id)]
            item['rank'] = record.xpath('rank/text()').extract_first()
            item['member_abbrname'] = record.xpath('shortname/text()').extract_first().strip()
            item['partyid'] = record.xpath('partyid/text()').extract_first().strip()
            item['volume'] = record.xpath('volume/text()').extract_first()
            item['change_volume'] = record.xpath('varVolume/text()').extract_first()
            yield item