# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from TheBeastSpider.settings import SQL_DATE_TIME_FORMAT, SQL_DATE_FORMAT


class ThebeastItemLoader(ItemLoader):
    # 自定义itemLoader
    default_output_processor = TakeFirst()


def clean_tag(value):
    # 去除数据中的特殊字符
    line = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥¥%……&*（）]+', "", value)
    return line


def clean_strip(value):
    # 清除空格和换行符
    value = (value.replace("\n", "")).replace("\r", "").strip()
    return value


def str_to_int(value):
    # 将字符串改为数字
    value = float(value) / 100.00
    return value


class ThebeastspiderItem(scrapy.Item):
    # 野兽派花艺
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(clean_tag, str_to_int),
    )
    style_notes = scrapy.Field(
        input_processor=MapCompose(clean_strip),
    )
    composition = scrapy.Field(
        input_processor=MapCompose(clean_strip),
    )
    inspiration = scrapy.Field(
        input_processor=MapCompose(clean_strip),
        output_processor=Join(","),
    )
    details = scrapy.Field(
        input_processor=MapCompose(clean_strip),
    )
    image_url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        sql = "INSERT INTO the_beast_flower(title,url,url_object_id,price,style_notes,composition,image_url,crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        if 'style_notes' not in self:
            self['style_notes'] = self['inspiration']
        if 'composition' not in self:
            self['composition'] = self['details']
        params = (
            self["title"], self['url'], self['url_object_id'], self['price'], self['style_notes'], self['composition'],
            self['image_url'], self['crawl_time'].strftime(SQL_DATE_TIME_FORMAT))
        return sql, params
