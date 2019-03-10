# -*- coding: utf-8 -*-
import pymysql

# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JdspiderPipeline(object):
    

    def open_spider(self, spider):
        MySQL_INFO = spider.settings['MYSQL']
        self.db = pymysql.connect(**MySQL_INFO)
        self.cursor = self.db.cursor()


    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


    def process_item(self, item, spider):
        keys, values = dict(item).keys(), dict(item).values()
        # try:
        #     self.cursor.execute("INSERT INTO books({}) VALUES ({});".format(",".join(keys), "'" + "','".join(values) + "'"))
        #     self.db.commit()
        # except Exception as e:
        #     self.db.rollback()
        #     print(e)
        return item