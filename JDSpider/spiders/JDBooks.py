# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
from JDSpider.items import JdspiderItem
from scrapy_redis.spiders import RedisSpider


class JdbookSpider(RedisSpider):
    name = 'JDBooks'
    allowed_domains = ['book.jd.com','list.jd.com','c0.3.cn', 'item.jd.com']
    redis_key = "bookpages:page_urls"


    # 分析商品列表页面
    def parse(self, response):
        cat = re.findall('cat=(.*?)&', response.request.url)[0]
        lis = response.xpath("//li[@class='gl-item']//div[@class='p-name']/a")
        for li in lis:
            book_detail_link = 'https:' + li.xpath("./@href").extract_first()
            skuId = re.findall("[0-9]{8}", book_detail_link)[0]
            yield scrapy.Request(
                book_detail_link,
                callback=self.parse_detail,
                meta={
                    'skuId':skuId,
                    'cat':cat
                }
            )


    # 分析商品详情页面
    def parse_detail(self, response):
        item = JdspiderItem()
        item['collect_date'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['url'] = response.request.url
        item['cat'] = response.meta['cat']
        item['skuId'] = response.meta['skuId']
        item['title'] = response.xpath("//div[@class='item ellipsis']/text()").extract_first()
        lis = response.xpath("//div[@class='p-parameter']/ul/li")
        item['publish'],item['ISBN'],item['edition'],item['brand'],item['series_name'],item['publish_date'] = "","","","","",""
        for li in lis:
            desc = re.sub('\r|\n|\t|\s','',li.xpath("string(.)").extract_first())
            item['publish'] = desc.split('：')[1] if desc.count('出版社') else item['publish']
            item['ISBN'] = desc.split('：')[1] if desc.count('ISBN') else item['ISBN']
            item['edition'] = desc.split('：')[1] if desc.count('版次') else item['edition']
            item['brand'] = desc.split('：')[1] if desc.count('品牌') else item['brand']
            item['series_name'] = desc.split('：')[1] if desc.count('丛书名') else item['series_name']
            item['publish_date'] = desc.split('：')[1] if desc.count('出版时间') else item['publish_date']
        
        yield scrapy.Request(
            "https://c0.3.cn/stock?skuId={}&cat={}&area=1_72_4137_0".format(item['skuId'], item['cat']),
            callback=self.get_other_info,
            meta={'item': item},
            dont_filter=False
        )


    def get_other_info(self, response):

        item = response.meta['item']
        info = json.loads(response.body.decode('GBK'))
        item['stockDesc'] = re.findall("<strong>(.*?)</strong>",info['stock']['stockDesc'])[0]
        item['current_price'] = info['stock']['jdPrice']['op'] if 'jdPrice' in info['stock'] else ""
        item['original_price'] = info['stock']['jdPrice']['m'] if 'jdPrice' in info['stock'] else ""
        print(item)
        yield item

