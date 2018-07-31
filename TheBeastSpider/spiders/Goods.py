# -*- coding: utf-8 -*-
import scrapy
import time
from urllib import parse
from scrapy.http import Request
from selenium import webdriver
from TheBeastSpider.items import ThebeastItemLoader, ThebeastspiderItem
from TheBeastSpider.utils.common import get_md5, con_dic
import datetime
# scrapy 信号
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class GoodsSpider(scrapy.Spider):
    name = 'Goods'
    allowed_domains = ['www.thebeastshop.com']
    start_urls = con_dic('http://www.thebeastshop.com/item/cate/', ['fr', 'ht', 'hd', 'tt', 'pc', 'frag', 'jw', 'lg'],
                         'htm')
    # start_urls = ['http://www.thebeastshop.com/item/cate/fr.htm','http://www.thebeastshop.com/item/cate/ht.htm',]
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"

    headers = {
        "HOST": "www.thebeastshop.com",
        "Referer": "http://www.thebeastshop.com",
        "User-Agent": agent
    }

    handle_httpstatus_list = [200,404]

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 150,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': Login.get_session(),
            'Cookie': 'ref=yes; newbsut=2205185297873952; ac=AC0553; ztqvode=b96b2d70c4e487ee7dcc9bd66dbd639a; Hm_lvt_7c10355ee0f6b21af208947325fd4ad7=1522225099,1522225442,1522243383,1522308486; behe_reach=9; bh_mnid=b329c77f-3582-44cc-a26b-144a71438d53_8; Hm_lpvt_7c10355ee0f6b21af208947325fd4ad7=1522320794; JSESSIONID=08BE40E0988D1039777C04C544A273CB',
            'Host': 'www.thebeastshop.com',
            'Referer': 'http://www.thebeastshop.com/item/cate/fr.htm',
            'Upgrade-Insecure-Requests': 1,
            "User-Agent": agent
        }
    }

    # 每个spider调用一个chrome，方便多线程处理
    def __init__(self):
        self.brower = webdriver.Chrome(executable_path="D:/python/chromedriver.exe")
        super(GoodsSpider, self).__init__()
        # 通过signals实现信号传递
        dispatcher.connect(self.spider_close, signals.spider_closed)
        # 收集数据
        self.success_url = []
        self.fail_url = []

    def spider_close(self, spider):
        # 当爬虫关闭时，自动关闭chrome
        self.crawler.stats.set_value("fail_url", ",".join(self.fail_url))
        self.crawler.stats.set_value("success_url", ",".join(self.success_url)) 
        print("spider close")
        self.brower.quit()

    def parse(self, response):
        """
        1、获取文章列表页中的文章url并交给scrapy 下载后并进行解析
        2、获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        # 提取所有URL
        if response.status == 200:
            self.success_url.append(response.url)
            self.crawler.state.inc_value("success_url")
        if response.status == 404:
            self.fail_url.append(response.url)
            self.crawler.state.inc_value("fail_url")

        url_node = response.css(".main #product_list .block_product .product-name a")
        for url in url_node:
            post_url = url.css("::attr(href)").extract_first()
            # 通过PARSE函数进行url拼接
            print(post_url)
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_item, headers=self.headers,
                          dont_filter=True)

    def parse_item(self, response):
        item_loader = ThebeastItemLoader(item=ThebeastspiderItem(), response=response)
        item_loader.add_css("title", "#product_intro .product_name::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("price", "#product_intro #showPrice span::text")
        item_loader.add_xpath("style_notes", "//*[@id='product_intro']/div[13]/p/text()")
        item_loader.add_xpath("composition", "//*[@id='product_intro']/div[14]/p/text()")
        item_loader.add_xpath("inspiration", "//*[@id='product_intro']/div[15]/p/text()")
        item_loader.add_xpath("details", "//*[@id='product_intro']/div[16]/p/text()")
        item_loader.add_css("image_url", "#product_img img::attr(src)")
        item_loader.add_value("crawl_time", datetime.datetime.now())

        article_item = item_loader.load_item()

        return article_item
