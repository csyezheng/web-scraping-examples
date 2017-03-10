#-*- encoding:utf8 -*-

import scrapy


class MaginSpider(scrapy.Spider):

    name = 'sse_magin_announcement'

    def start_requests(self):
        url = 'http://www.sse.com.cn/disclosure/magin/announcement/ssereport/s_index.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Referer': 'http://www.sse.com.cn/disclosure/magin/announcement/'
                   }
        return scrapy.Request(url=url, headers=headers, meta={'headers': headers}, callback=self.real_requests)

    def real_requests(self, response):
        announcements = response.xpath('//dd')
        headers = response.meta['headers']
        for announcement in announcements:
            url = announcement.xpath('a/@href').extract_first()
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

        page_index = response.xpath('//div[@class="createPage"]/@page_index').extract_first()
        page_count = response.xpath('//div[@class="createPage"]/@page_count').extract_first()
        new_index = page_index + 1
        if new_index <= page_count:
            url = 'http://www.sse.com.cn/disclosure/magin/announcement/s_index_{0}.htm'.format(new_index)
            yield scrapy.FormRequest(url=url, headers=headers, callback=self.real_requests)

    def parse(self,response):
        article = response.css('div.article-infor')
        title = article.xpath('h2/text()').extract_first()
        announ_date = article.css('.article_opt').xpath('i/text()').extract_first()
        
