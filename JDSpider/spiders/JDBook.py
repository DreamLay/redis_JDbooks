# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
from JDSpider.items import JdspiderItem


class JdbookSpider(scrapy.Spider):
    name = 'JDBook'
    allowed_domains = ['book.jd.com','list.jd.com','c0.3.cn', 'item.jd.com']
    start_urls = ['http://book.jd.com/booksort.html']


    def start_requests(self):
        yield scrapy.Request(
            'http://book.jd.com/booksort.html',
            callback=self.parse_category
        )


    # 分析商品分类页面
    def parse_category(self, response):
        dts = response.xpath("//div[@class='mc']//dt")
        dds = response.xpath("//div[@class='mc']//dd")
        for i in range(len(dts)):
            father_name = dts[i].xpath("./a/text()").extract_first()
            # father_url = dts[i].xpath("./a/@href").extract_first()
            children = dds[i].xpath(".//a")
            for child in children:
                child_name = child.xpath("./text()").extract_first()
                child_url = 'https:' + child.xpath("./@href").extract_first()

                yield scrapy.Request(
                    child_url,
                    callback=self.parse_books_list,
                    meta={"father_category": father_name, "category": child_name},
                    dont_filter=False
                )
                break
            break
 
        

    # 分析商品列表页面
    def parse_books_list(self, response):
        father_name, child_name = response.meta['father_category'],response.meta['category']
        cat = re.findall("cat=(.*?)&",response.request.url)[0]
        lis = response.xpath("//li[@class='gl-item']//div[@class='p-name']/a")
        for li in lis:
            book_detail_link = 'https:' + li.xpath("./@href").extract_first()
            skuId = re.findall("[0-9]{8}", book_detail_link)[0]
            yield scrapy.Request(
                book_detail_link,
                callback=self.parse,
                meta={
                    "cat":cat, "skuId":skuId,
                    "father_category":father_name,
                    "category":child_name,
                    },
                dont_filter=False    
                
            )

        # 翻页
        next_page_link = 'https://list.jd.com' + response.xpath("//a[@class='pn-next']/@href").extract_first() if response.xpath("//a[@class='pn-next']/@href").extract_first() else None
        if next_page_link:
            yield scrapy.Request(
                next_page_link,
                callback=self.parse_books_list,
                meta={"father_category": father_name, "category": child_name}
            )


    # 分析商品详情页面
    def parse(self, response):

        item = JdspiderItem()
        item['collect_date'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['father_category'] = response.meta['father_category']
        item['category'] = response.meta['category']
        item['url'] = response.request.url
        item['cat'] = response.meta['cat']
        item['skuId'] = response.meta['skuId']
        item['title'] = response.xpath("//div[@class='item ellipsis']/text()").extract_first()
        lis = response.xpath("//div[@class='p-parameter']/ul/li")
        item['publish'],item['ISBN'],item['edition'],item['brand'],item['series_name'],item['publish_date'] = "","","","","",""
        for li in lis:
            desc = re.sub('\r|\n|\t|\s','',li.xpath("string(.)").extract_first())
            # print(desc.split('：'))
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
        # print(item)
        yield item

