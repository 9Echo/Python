# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZuFangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名字
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 出租方式
    way_of_rent = scrapy.Field()
    # 详情:几室几厅、面积、朝向、楼层、装修
    detail = scrapy.Field()
    # 具体房屋信息页面url
    origin_url = scrapy.Field()


class ESFHouseItem(scrapy.Item):
    # 城市
    city = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 小区名字
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 详情:几室几厅、面积、朝向、楼层、装修
    detail = scrapy.Field()
    # 具体房屋信息页面url
    origin_url = scrapy.Field()

