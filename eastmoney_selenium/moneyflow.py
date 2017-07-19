#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from lxml import etree

import pymysql.cursors
from datetime import datetime


def get_stocks():
    """Get a list about stock code"""
    
    connection = pymysql.connect(host='192.168.31.181',
                             user='ope1',
                             password='Siteope',
                             db='stock',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    code_list = []
    try:
        with connection.cursor() as cursor:
            sql = 'select stock_code from code_stocka_wind'
            cursor.execute(sql,())
            records = cursor.fetchall()
            for record in records:
                stock_code = record['stock_code'].split('.')[0]
                code_list.append(stock_code)
    finally:
        connection.close()
    return code_list



def get_data(stock_code):
    """To get money input and output for special stock code"""
 
    now_url = 'http://data.eastmoney.com/zjlx/{0}.html'.format(stock_code)
    driver = webdriver.PhantomJS()
    driver.get(now_url)
    time.sleep(3)
    
    # elem = driver.find_element_by_css_selector('div.flash-legendrt')

    pageSource = driver.page_source
    #bsObj = BeautifulSoup(pageSource, 'lxml')

    #table = bsObj.find("div", {"class": "content2"}).find("table")
    #print(table.find("span").get_text())

    
    selector = etree.HTML(pageSource)
    tr_list = selector.xpath('//div[@class="flash-legendrt"]//tr')[1:]
    
    item = {}
    for index, tr in enumerate(tr_list):
        td_list = tr.xpath('td//text()')

        if index == 0:
            field = "super"
        elif index == 1:
            field = "big"
        elif index == 2:
            field = "middle"
        else:
            field = "small"
                
        temp = []
        for td in td_list:
            td = td.replace('\n','').replace(' ','')
            if td:
                temp.append(td)

        item[field + '_in'] = temp[1] + temp[2]
        item[field + '_out'] = temp[3] + temp[4]
        
    item['stock_code'] = stock_code
    driver.close()
    print(item)
    return item


def store_data(item):
    """store data into database"""

    conn = pymysql.connect(host='192.168.31.181',
                           user='ope1',
                           password='Siteope',
                           db='test',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    trade_date = datetime.now()
    stock_code = item.get('stock_code')
    super_in = item.get('super_in')
    super_out = item.get('super_out')
    big_in = item.get('big_in')
    big_out = item.get('big_out')
    middle_in = item.get('middle_in')
    middle_out = item.get('middle_out')
    small_in = item.get('small_in')
    small_out = item.get('small_out')
    try:
        with conn.cursor() as cur:
            insert_sql = '''insert into `eastmoney_zjlx` (`trade_date`, `stock_code`, `super_in`,
                          `super_out`, `big_in`, `big_out`, `middle_in`, `middle_out`, `small_in`,
                          `small_out`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(insert_sql, (trade_date, stock_code, super_in, super_out, big_in, big_out,
                                        middle_in, middle_out, small_in, small_out))
        conn.commit()
    finally:
        conn.close()


def main():
    stock_list = get_stocks()
    for stock in stock_list:
        item = get_data(stock)
        store_data(item)
        

if __name__ == "__main__":
    main()
