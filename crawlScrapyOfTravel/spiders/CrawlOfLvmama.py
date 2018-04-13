# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlScrapyOfTravel.items import TreavalItem
from crawlScrapyOfTravel.util import SpiderUtil
import re

class CrawloflvmamaSpider(CrawlSpider):
    name = 'CrawlOflvmama'
    allowed_domains = ['lvmama.com']
    start_urls = ['http://s.lvmama.com/route/H56K321000?keyword=yunnan&k=0#list']

    # 每页翻页的匹配规则
    pagelink = LinkExtractor(allow=(r"[A-Za-z0-9]+\?keyword=.*#list"),attrs="onclick")#,process_value="pagelinkvalue"
    # 每条记录的匹配规则
    contentlink = LinkExtractor(allow=(r"http://dujia.lvmama.com/[a-z]+/([a-z0-9]+-D56|\d+)"))

    rules = (
        # 本案例的url被web服务器篡改，需要调用process_links来处理提取出来的url
        Rule(pagelink, process_links="deal_pagelinks", follow=True),
        Rule(contentlink, callback="parse_item", follow=True)
    )

    def deal_pagelinks(self, links):
        for pagelink in links:
            lnk = re.search(r'http://s.lvmama.com/route/routeSelectAjax\("s<lvmama<com>route>([A-Za-z0-9]+\?keyword=.*#list)"\)', pagelink.url)
            pagelink.url = 'http://s.lvmama.com/route/'+lnk.group(1)
        return links

    # links 是当前response里提取出来的链接列表
    def deal_links(self, links):
        for each in links:
            print each
            each.url ="http://s.lvmama.com/route/"+ each
        return links

    def parse_item(self, response):
        item = TreavalItem()
        # 标题
        item['title'] = SpiderUtil.listIsEmpty(response.xpath("//h1/b/text()").extract())[0]
        # 简介
        item['introduction'] = ''
        jj = SpiderUtil.listIsEmpty(response.xpath("//h1/text()").extract())
        for j in jj:
            item['introduction'] += SpiderUtil.superstrip(j)
        # 详细描述
        detail = SpiderUtil.listIsEmpty(response.xpath("//div[@class='product-summary']/ul/li/text()").extract())
        item['detail']=''
        for li in detail:
            if li.strip() == '':
                continue
            else:
                item['detail'] += "["+SpiderUtil.superstrip(li)+"]"

        # 营业时间
        # item['business_time'] = response.xpath()
        # 标签
        # item['label'] = response.xpath()
        # 酒店
        # item['hotel'] = response.xpath()
        # 价格
        item['price'] = SpiderUtil.listIsEmpty(
            response.xpath('//span[@class="price_num"]/dfn/text()').extract())[0]
        # 评价
        # item['comment'] = response.xpath()
        # 星级
        stars = SpiderUtil.listIsEmpty(response.xpath("//h1[@class='detail_product_tit']/a/span/@class").extract())[0]
        if "one" in stars:
            item['star'] = 1
        elif "two" in stars:
            item['star'] = 2
        elif "three" in stars:
            item['star'] = 3
        elif "four" in stars:
            item['star'] = 4
        elif "five" in stars:
            item['star'] = 5
        else:
            item['star'] = 0

        numberOfpeople = SpiderUtil.listIsEmpty(response.xpath("//a[@id='appraise']/span/i/text()").extract())
        # 出游人数
        item['numberOfout'] = SpiderUtil.emptyStrToZero(numberOfpeople[0])
        # 评价人数
        item['numberOfcomment'] = SpiderUtil.emptyStrToZero(numberOfpeople[1])
        # 满意度
        item['satisfaction'] = SpiderUtil.listIsEmpty(response.xpath("//div[@class='product_top_price_box']/div/div[@class='product_top_dp_left']/span/text()").extract())[0]

        # 链接
        item['url'] = response.url

        if "group" in response.url:
            item['mode'] = "跟团游"
        elif "local" in response.url:
            item['mode'] = "落地团"
        elif "free" in response.url:
            item['mode'] = "自由行"
        else:
            item['mode'] = ""

        yield item
