#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy import cmdline

path = '/home/csyezheng/Documents/baiinfo_news'
cmdline.execute('scrapy crawl baiinfo_news -a path={0}'.format(path).split())