# -*- coding: utf-8 -*-

import scrapy
import re
from new.items import ZuFangItem
from new.items import ESFHouseItem


class DemoSpider(scrapy.Spider):
    name = 'demo'
    # allowed_domains = ['5i5j.com']
    start_urls = ['https://www.5i5j.com']

    def parse(self, response):
        try:
            city_infos = response.xpath("//p[contains(@class,'city')]//a")
            # 获取城市名字和城市主页链接
            for city_info in city_infos:
                city_name = city_info.xpath(".//text()").get()
                city_url = city_info.xpath(".//@href").get()
                # 构建租房链接
                zufang_url = city_url + "/zufang"
                # 构建二手房链接
                esf_url = city_url + "/ershoufang"
                yield scrapy.Request(url=zufang_url, callback=self.parse_zufang, dont_filter=True, meta={"info": city_name, "url": (zufang_url)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, dont_filter=True, meta={"info": (city_name), "url": (esf_url)})
        except Exception as e:
            print(e)

    def parse_zufang(self, response):
        try:
            zufang_url = response.meta.get('url')
            city_name = response.meta.get('info')
            liList = response.xpath("//div[@class='list-con-box']/ul/li")
            print("*******************************************")
            print(zufang_url)
            print("*******************************************")
            for li in liList:
                origin_url = li.xpath(".//div[@class='listCon']//a/@href").get().split("/")[-1]
                origin_url = response.urljoin(origin_url)
                # 获取小区
                name = li.xpath(".//div[@class='listX']//a/text()").get().strip()
                name = re.sub(r"\s", "", name)
                # 获取几室几厅、面积、朝向、楼层、装修
                detail = li.xpath(".//div[@class='listX']//p/text()").get().strip()
                detail = re.sub(r"\s", "", detail)
                # 获取价格
                price = li.xpath(".//div[@class='jia']//strong/text()").get()
                unit = li.xpath(".//div[@class='jia']/p[1]/text()").get()
                unit = re.sub(r"\s", "", unit)
                price = price + unit
                # 获取出租方式
                way_of_rent = li.xpath(".//div[@class='jia']//p[2]/text()").get().split("：")[-1]

                item = ZuFangItem(city=city_name, name=name, price=price, way_of_rent=way_of_rent, detail=detail,
                                  origin_url=origin_url)
                yield item
                # 下一页的URL链接
            next_url = response.xpath("//div[contains(@class,'pageSty')]//a[@class='cPage']/@href").get()
            # 如果还有下一页，继续调用该函数
            if next_url:
                yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_zufang,
                                     meta={"info": city_name, "url": (zufang_url)})
        except Exception as e:
            print(e)

    def parse_esf(self, response):
        try:
            city_name = response.meta.get('info')
            esf_url = response.meta.get('url')
            print("*******************************************")
            print("*******************************************")
            liList = response.xpath("//div[@class='list-con-box']/ul/li")
            for li in liList:
                # 标题
                title = li.xpath(".//h3[@class='listTit']//a/text()").get().strip()
                # 详情URL得到的是/ershoufang/xxxxxxxx.html
                # 调用函数自动合成完整的URL
                origin_url = li.xpath(".//h3[@class='listTit']//a/@href").get()
                origin_url = response.urljoin(origin_url)
                # 小区名字
                name = li.xpath(".//div[@class='listX']//a/text()").get().strip()
                name = re.sub(r"\s", "", name)
                # 详情信息
                detail = li.xpath(".//div[@class='listX']/p[1]/text()").get().strip()
                # 去掉空格
                detail = re.sub(r"\s", "", detail)
                # 价格
                price = li.xpath(".//div[@class='jia']//strong/text()").get()
                # 单位
                unit = li.xpath(".//div[@class='jia']//p[1]/text()").get().strip()
                # 得到的是字符串类型可直接拼接
                price = price + unit
                # 单价
                unit_price = li.xpath(".//div[@class='jia']//p[2]/text()").get()
                item = ESFHouseItem(title=title, city=city_name, name=name, unit_price=unit_price, price=price,
                                    detail=detail, origin_url=origin_url)
                yield item
                # 下一页的URL链接得到的是/ershoufang/n2/
                # 链接不完整还要自己拼
            next_url = response.xpath("//div[contains(@class,'pageSty')]//a[@class='cPage']/@href").get()
            # 如果还有下一页，继续调用该函数
            if next_url:
                yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,
                                     meta={"info": (city_name), "url": (esf_url)})
        except Exception as e:
            print(e)





