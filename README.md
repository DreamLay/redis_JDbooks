# 设计一个简单的redis分布式集群爬虫

- **环境：**

  > 两台实体机：Macos Mojave, ubuntu 18

  > python==3.6, scrapy==1.5.1, scrapy-redis==0.6.8



- **说明**

  - 基于scrapy-redis分布式爬取J东每个分类下的图书。

  - 京东的图书还是很多的，关大类就有近60类，每个大类下面至少有五个小类，目测平均十三小类，每个小类下有100-300页商品，每页60个商品，算下来有近千万的商品。

  - 虽然比起所有商品数量或者某宝只是冰山一角，但是这个量级使用分布式还是很有必要的，能<font color="red">**提高爬取速度，提高查重性能，实现可持续断点续爬，实现多设备同时运行，提高系统稳健性**</font>。在我开发过程中试用一个进程（多线程）跑单个小分类大约1w4件商品需要一个下午，说明一下我的是联通百兆宽带，不是有线，数据量不大，估计时间都浪费在延迟上了。

    

- **其他**

  - 因为本人有一笔记本和一台台式，就直接物理模仿两台机器，ubuntu作为master服务，macos做slaver服务。本来想两台实体机再各装一套虚拟机实现一主三从，后来想到还要装两次环境嫌麻烦还是算了。

    其实一台机器开多个端口一样能实现模拟许多主从服务，只是这样没那么爽罢了，到时候加个哨兵再kill掉master试试，这样可以防止master挂掉。



- **流程**

  > `./spiders/JDBook_pages.py `  爬取每某小类某一页放进redis `key==bookpages:page_urls` 等待。

  > `./spiders/JDBooks.py` 从redis key==bookpages:page_urls 取url并删除。

  > 每次抓到新的url、请求体、请求method会进行sha1编码加密生成指纹拿去 `key==xxx:dupefilters` 中查找是否存在，不存在的话放入待请 求 `key==xxx:requests` 中并将指纹存入 `key==xxx:dupefilters`。



- **问题**

  运行爬虫时偶尔会报连接被拒绝的错误，网上查了也都是端口没放通之类的问题，但这个问题在我这根本不存在，毕竟都能存储数据了不存在端口限制，后来想想可能是我两台都是连着wifi，即使是局域网也会偶尔断连毕竟是无线，只是平时上上网感受不到，这点纯猜测。

  ```
  redis.exceptions.ConnectionError: Error 61 connecting to 192.168.31.229:6379. Connection refused.
  ```


Author:Laijy