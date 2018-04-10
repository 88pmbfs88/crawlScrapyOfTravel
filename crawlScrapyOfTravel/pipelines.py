# -*- coding: utf-8 -*-

from crawlScrapyOfTravel import settings
import mysql.connector
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlscrapyoftravelPipeline(object):

    def __init__(self):
         config = {
            'host': settings.MYSQL_HOST,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWD,
            'port': settings.MYSQL_PORT,
            'database': settings.MYSQL_DBNAME,
            'charset': 'utf8',
            'buffered': True
            }
         try:
            self.cnn = mysql.connector.connect(**config)
         except mysql.connector.Error as e:
            print 'connect fails!{}'.format(e)
         # 通过cursor执行增删查改
         self.cursor = self.cnn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into tuniusource(title, introduction, price, satisfaction ,star, brand, numberOfout, numberOfcomment, url, dayOfplay, isnew)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['title'],
                 item['introduction'],
                 item['price'],
                 item['satisfaction'],
                 item['star'],
                 item['brand'],
                 item['numberOfout'],
                 item['numberOfcomment'],
                 item['url'],
                 item['dayOfplay'],
                 item['isnew']
                 # item[''],
                 # item['']),
            ))

            # 提交sql语句
            self.cnn.commit()
        except Exception as error:
            print error

        return item
