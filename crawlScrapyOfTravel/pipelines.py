# -*- coding: utf-8 -*-

from crawlScrapyOfTravel import settings
# import mysql.connector
import MySQLdb
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlscrapyoftravelPipeline(object):

    def __init__(self):
         try:
            self.cnn = MySQLdb.connect(host=settings.MYSQL_HOST,
                                       port=settings.MYSQL_PORT,
                                       user=settings.MYSQL_USER,
                                       passwd=settings.MYSQL_PASSWD,
                                       db=settings.MYSQL_DBNAME,
                                       charset="utf8")

         except Exception as e:
            print 'connect fails!{}'.format(e)
         # 通过cursor执行增删查改
         self.cursor = self.cnn.cursor()

    def process_item(self, item, spider):
        if spider.name == "CrawlOftuniu":
            try:
                self.cursor.execute(
                    """insert into tuniu_source(title, introduction, price, satisfaction ,star, brand, numberOfout, numberOfcomment, url, dayOfplay, isnew)
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
        elif spider.name == "CrawlOflvmama":
             try:
                self.cursor.execute(
                    """insert into lvmama_source(title, introduction, price, satisfaction ,star, detail, numberOfout, numberOfcomment, url, mode)
                    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (item['title'],
                     item['introduction'],
                     item['price'],
                     item['satisfaction'],
                     item['star'],
                     item['detail'],
                     item['numberOfout'],
                     item['numberOfcomment'],
                     item['url'],
                     item['mode']
                     # item[''],
                     # item['']),
                ))
                    # 提交sql语句
                self.cnn.commit()
             except Exception as error:
                print error
        return item
