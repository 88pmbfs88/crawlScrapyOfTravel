# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TreavalItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 简介
    introduction = scrapy.Field()
    # 详细描述
    detail = scrapy.Field()
    # 营业时间
    business_time = scrapy.Field()
    # 标签
    label = scrapy.Field()
    # 酒店
    hotel = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 满意度
    satisfaction = scrapy.Field()
    # 评价
    comment = scrapy.Field()
    # 星级
    star = scrapy.Field()
    # 品牌
    brand = scrapy.Field()
    # 出游人数
    numberOfout = scrapy.Field()
    # 评价人数
    numberOfcomment = scrapy.Field()
    # 天数
    dayOfplay = scrapy.Field()
    #链接
    url =  scrapy.Field()
    #新品
    isnew = scrapy.Field()
    #出行方式
    mode = scrapy.Field()