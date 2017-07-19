#!/usr/bin/env python
#-*- coding: utf8 -*-


from scrapy import cmdline
import datetime


today = datetime.date.today().strftime('%Y-%m-%d')
begin_date = '2016-01-01'
end_date = '2016-12-31'
cmdline.execute('scrapy crawl cffex_position_ranking -a begin_date={0} -a end_date={1}'.format(today, today).split())