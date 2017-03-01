#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import pymysql.cursors
import json

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

config_data = read_json('config.json')
stocks_host = config_data['stocks_host']
stocks_db = config_data['stocks_db']
stocks_user = config_data['stocks_user']
stocks_password = config_data['stocks_password']
stocks_table = config_data['stocks_table']
store_host = config_data['store_host']
store_db = config_data['store_db']
store_user = config_data['store_user']
store_password = config_data['store_password']
store_table = config_data['store_table']

def get_stocks():
    """Get a list about stock code"""

    connection = pymysql.connect(host=stocks_host,
                                 user=stocks_user,
                                 password=stocks_password,
                                 db=stocks_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    code_list = []
    try:
        with connection.cursor() as cursor:
            sql = 'select stock_code from {0}'.format(stocks_table)
            cursor.execute(sql, ())
            records = cursor.fetchall()
            for record in records:
                stock_code, sign = record['stock_code'].split('.')
                if sign == 'SH':
                    sign = '1'
                else:
                    sign = '2'
                stock_code += sign
                code_list.append(stock_code)
    finally:
        connection.close()
    return code_list

def parse(url):
    r = requests.get(url)
    lst = r.text.split('"')
    print(lst)
    raw_data = r.text.split('"')[1]
    data_lst = raw_data.split(',')
    item = dict()
    item['stock_code'] = data_lst[1]
    item['super_in'] = data_lst[8]
    item['super_out'] = data_lst[9]
    item['big_in'] = data_lst[12]
    item['big_out'] = data_lst[13]
    item['middle_in'] = data_lst[15]
    item['middle_out'] = data_lst[16]
    item['small_in'] = data_lst[19]
    item['small_out'] = data_lst[20]
    item['trade_date'] = data_lst[24]
    return item


def clear_data():
    """store data into database"""

    conn = pymysql.connect(host=store_host,
                           user=store_user,
                           password=store_password,
                           db=store_db,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cur:
            insert_sql = 'TRUNCATE TABLE `{0}'.format(store_table)
            cur.execute(insert_sql, ())
        conn.commit()
    finally:
        conn.close()


def store_data(item):
    """store data into database"""

    conn = pymysql.connect(host=store_host,
                           user=store_user,
                           password=store_password,
                           db=store_db,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    trade_date = item.get('trade_date')
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
            insert_sql = '''insert into `{0}` (`trade_date`, `stock_code`, `super_in`,
                          `super_out`, `big_in`, `big_out`, `middle_in`, `middle_out`, `small_in`,
                          `small_out`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(store_table)
            cur.execute(insert_sql, (trade_date, stock_code, super_in, super_out, big_in, big_out,
                                     middle_in, middle_out, small_in, small_out))
        conn.commit()
    finally:
        conn.close()


def main():
    stock_list = get_stocks()
    clear_data()
    for stock in stock_list:
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd={0}'.format(stock) + '&sty=CTBFTA&st=z&sr=&p=&ps=&cb=&js=var%20tab_data=({data:[(x)]})&token=70f12f2f4f091e459a279469fe49eca5'
        item = parse(url)
        store_data(item)


if __name__ == "__main__":
    main()
