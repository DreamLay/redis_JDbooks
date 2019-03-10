# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
from JDSpider.items import JdspiderItem


class JdbookSpider(scrapy.Spider):
    name = 'pages'
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
        # 翻页
        next_page_link = 'https://list.jd.com' + response.xpath("//a[@class='pn-next']/@href").extract_first() if response.xpath("//a[@class='pn-next']/@href").extract_first() else None
        print(next_page_link)
        if next_page_link:
            yield scrapy.Request(
                next_page_link,
                callback=self.parse_books_list,
                meta={"father_category": father_name, "category": child_name}
            )
