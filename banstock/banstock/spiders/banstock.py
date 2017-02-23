import scrapy
import logging
from decimal import Decimal
from lxml import etree
from ..items import BanstockItem

class banstockSpider(scrapy.Spider):
    name = "banstock"

    def start_requests(self):
        allowed_domains = ["gupiaodadan.com"]
        urls = [
            'http://www.gupiaodadan.com/banstock-40'
        ]
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                      Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        records = response.xpath('//div[@id = "emailelert"]//tr')[1:]
        for record in records:
            item = BanstockItem()
            try:
                result = record.xpath('./td//text()').extract()
                item['rank'] = int(result[0])
                item['code'] = result[1]
                item['name'] = result[2]
                item['buy'] = int(''.join(result[3].split(',')))
                item['sell'] = int(''.join(result[4].split(',')))
                item['price'] = float(''.join(result[5].split(',')))
                item['change'] = float(''.join(result[6].split(',')))
                logging.info(item)
            except Exception:
                pass
            yield item
