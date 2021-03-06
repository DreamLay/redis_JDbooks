# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    skuId = scrapy.Field()
    title = scrapy.Field()
    # father_category = scrapy.Field()
    # category = scrapy.Field()
    cat = scrapy.Field()
    url = scrapy.Field()
    publish = scrapy.Field()
    ISBN = scrapy.Field()
    edition = scrapy.Field()
    brand = scrapy.Field()
    series_name = scrapy.Field()
    publish_date = scrapy.Field()
    stockDesc = scrapy.Field()
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    collect_date = scrapy.Field()

