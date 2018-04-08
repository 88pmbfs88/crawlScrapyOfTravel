# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlScrapyOfTravel.items import TuNiuItem


class CrawloftuniuSpider(CrawlSpider):
    name = 'CrawlOftuniu'
    allowed_domains = ['tuniu.com']
    start_urls = ['http://s.tuniu.com/search_complex/whole-yz-0-yunnan/1']

   # 每页翻页的匹配规则
    pagelink = LinkExtractor(allow=(r"/search_complex/whole-yz-0-yunnan/\d+"))
    # 每条记录的匹配规则
    contentlink = LinkExtractor(allow=(r"//www.tuniu.com/tour/\d+"))

    rules = (
        # 本案例的url被web服务器篡改，需要调用process_links来处理提取出来的url
        Rule(pagelink, process_links = "deal_links"),
        Rule(contentlink, callback = "parse_item")
    )

    # links 是当前response里提取出来的链接列表
    def deal_links(self, links):
        for each in links:
            each.url ="http://s.tuniu.com"+ each
        return links

    def parse_item(self, response):
        item = TuNiuItem()
        full_title = response.xpath('//h1[@class="resource-title"]/strong/text()').extract()[0]
        # 标题
        item['title'] = full_title.split('>')[0]
        # 简介
        item['introduction'] =  full_title.split('>')[1]
        # 详细描述
        # item['detail'] = response.xpath()
        # 营业时间
        # item['business_time'] = response.xpath()
        # 标签
        # item['label'] = response.xpath()
        # 酒店
        # item['hotel'] = response.xpath()
        # 价格
        item['price'] = response.xpath('//span[@class="price-quantity"]/span[@class="price-number"]/text()').extract()[0]
        # 满意度
        item['satisfaction'] =  response.xpath('//div[@class="resource-statisfaction"]/a[@class="resource-statisfaction-number"]/text()').extract()[0]
        # 评价条数
        # item['comment'] = response.xpath()
        # 星级
        item['star'] = len(response.xpath('//*[@id="J_basisStar"]/i').extract())
        # 品牌
        band = response.xpath('//a[@class="resource-supplier-name"]/strong/text()').extract()
        if len(band) != 0:
            item['brand'] = band[0]
        else:
            item['brand'] = ' '

        numberOfpeople = response.xpath('//*[@class="resource-people-number"]/text()').extract()[0]
        # 出游人数
        item['numberOfout'] = numberOfpeople[0]
        # 评价人数
        item['numberOfcomment'] = numberOfpeople[1]
        #链接
        item['url'] =  response.url
        # 游玩天数
        item['dayOfplay'] = response.xpath('//div[@id="J_Detail"]/div[@class="detail-sections"]/div[@class="J_DetailFeature section-box detail-feature"]/div[@class="section-box-body"]/div[@class="section-box-content"][1]/div[@class="detail-feature-brief"]/div[@class="detail-feature-brief-item"][1]/strong/text()').extract()[0]

        # # 内容，先使用有图片情况下的匹配规则，如果有内容，返回所有内容的列表集合
        # content = response.xpath('//div[@class="contentext"]/text()').extract()
        # # 如果没有内容，则返回空列表，则使用无图片情况下的匹配规则
        # if len(content) == 0:
        #     content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
        #     item['content'] = "".join(content).strip()
        # else:
        #     item['content'] = "".join(content).strip()
        # # 链接
        # item['url'] = response.url

        yield item

