# -*- coding: utf-8 -*-


BOT_NAME = 'JDSpider'

SPIDER_MODULES = ['JDSpider.spiders']
NEWSPIDER_MODULE = 'JDSpider.spiders'

LOG_LEVEL = 'WARNING'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"   # 去重类指定
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 调度器
# 持久化，程序关了以后，内容数据保留，下一次启动会继续
SCHEDULER_PERSIST = True

ITEM_PIPELINES = {
   'JDSpider.pipelines.JdspiderPipeline': 300,
}

MYSQL = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '1234',
    'db': 'jdstore',
    'charset': 'utf8'
}

REDIS_HOST = "192.168.31.229"
REDIS_PORT = "6379"
REDIS_PARAMS = {
    'password':'1234'
}