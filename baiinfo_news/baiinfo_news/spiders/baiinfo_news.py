# -*- coding: utf-8 -*-

import scrapy
from ..pdf2txt import readPDF
import os

class BaiInfoNews(scrapy.Spider):
    name = 'baiinfo_news'

    def start_requests(self):
        url = 'http://www.baiinfo.com/Orders/NewsList/7704'
        headers = {'Referer': 'http://www.baiinfo.com/yjbg/yanjiugaobao',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                                 'Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36'}
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        news_list = response.xpath('//div[@class="news_more_left"]/ul/li')
        for news in news_list:
            title = news.xpath('a//text()').extract_first().replace('/', '-')
            url = news.xpath('a/@href').extract_first()
            publish_date = news.xpath('span/text()').extract_first()
            headers = {'Referer': 'http://www.baiinfo.com/yjbg/yanjiugaobao',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                                     'Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36'}
            if 'Orders' in url:
                url = 'http://www.baiinfo.com' + url
            yield scrapy.Request(url,
                                 headers=headers,
                                 meta={'title': title, 'publish_date': publish_date},
                                 callback=self.detail_parse)

        page_info = response.xpath('//div[@class="news_tel_4"]/ul/div/a')
        for curr in page_info:
            page_indentify = curr.xpath('text()').extract_first()
            if page_indentify == '下一页':
                next_page = 'http://www.baiinfo.com' + curr.xpath('@href').extract_first()
                headers = {'Referer': 'http://www.baiinfo.com/yjbg/yanjiugaobao',
                           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                                         'Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36'}
                yield scrapy.Request(next_page, headers=headers, callback=self.parse)

    def detail_parse(self, response):
        title = response.meta['title']
        publish_date = response.meta['publish_date']
        file_dir = self.path + '/' + publish_date
        self.logger.info(publish_date)
        self.logger.info(title)

        file_path = self.path + '/' + publish_date + '/' + title         # no include extention
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        content = ''.join(response.xpath('//ul[@class="news_tel_z"]//text()').extract())
        if '点击下载' in content:
            pdf_url = response.xpath('//ul[@class="news_tel_z"]/div[@class="news_tex"]//a/@href').extract_first()
            headers = {'Referer': 'http://www.baiinfo.com/yjbg/yanjiugaobao',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                                     'Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36'}
            yield scrapy.Request(pdf_url, headers=headers, meta={'file_path': file_path}, callback=self.downloads)
        else:
            with open(file_path+'.txt', 'w') as f:
                f.write(content)

    def downloads(self, response):
        file_path = response.meta['file_path']
        with open(file_path+'.pdf', 'wb') as f:
            f.write(response.body)
        ret = readPDF(file_path+'.pdf')
