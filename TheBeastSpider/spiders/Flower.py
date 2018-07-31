# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TheBeastSpider.items import ThebeastItemLoader, ThebeastspiderItem
from TheBeastSpider.utils.common import get_md5
import datetime
#from TheBeastSpider.utils import Login


class FlowerSpider(CrawlSpider):
    name = 'Flower'
    allowed_domains = ['www.thebeastshop.com']
    start_urls = ['http://www.thebeastshop.com']
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    headers = {
        "HOST": "www.thebeastshop.com",
        "Referer": "http://www.thebeastshop.com",
        "User-Agent": agent
    }

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Cookie': Login.get_session(),
            'Cookie': 'ref=yes; newbsut=2205185297873952; ac=AC0553; ztqvode=b96b2d70c4e487ee7dcc9bd66dbd639a; Hm_lvt_7c10355ee0f6b21af208947325fd4ad7=1522225099,1522225442,1522243383,1522308486; behe_reach=9; bh_mnid=b329c77f-3582-44cc-a26b-144a71438d53_8; Hm_lpvt_7c10355ee0f6b21af208947325fd4ad7=1522320794; JSESSIONID=08BE40E0988D1039777C04C544A273CB',
            'Host': 'www.thebeastshop.com',
            'Referer': 'http://www.thebeastshop.com/item/cate/fr.htm',
            'Upgrade-Insecure-Requests': 1,
            "User-Agent": agent
        }
    }

    rules = (
        Rule(LinkExtractor(allow=r'app/item/detail/\w+.htm'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     r = Request(url=link.url, callback=self._response_downloaded,dont_filter=True)
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r

    def parse_item(self, response):
        item_loader = ThebeastItemLoader(item=ThebeastspiderItem(), response=response)
        item_loader.add_css("title", "#product_intro .product_name::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("price", "#product_intro #showPrice span::text")
        item_loader.add_xpath("style_notes", "//*[@id='product_intro']/div[13]/p/text()")
        item_loader.add_xpath("composition", "//*[@id='product_intro']/div[14]/p/text()")
        item_loader.add_css("image_url", "#product_img img::attr(src)")
        item_loader.add_value("crawl_time", datetime.datetime.now())

        article_item = item_loader.load_item()

        return article_item
