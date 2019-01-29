# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pymysql
from scrapy import log
from new import settings
from new.items import ZuFangItem, ESFHouseItem

# 保存到json文件中


# class NewPipeline(object):
#     def __init__(self):
#         self.zufang_fp = open('zufang.json', 'wb')
#         self.esf_fp = open('esf.json', 'wb')
#         self.zufang_exporter = JsonLinesItemExporter(self.zufang_fp, ensure_ascii=False)
#         self.esf_exporter = JsonLinesItemExporter(self.esf_fp, ensure_ascii=False)
#
#     def process_item(self, item, spider):
#         self.zufang_exporter.export_item(item)
#         self.esf_exporter.export_item(item)
#         return item
#
#     def close_spider(self, spider):
#         self.zufang_fp.close()
#         self.esf_fp.close()

# 保存到数据库中


class MysqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == ZuFangItem:
            try:
                self.cursor.execute("""select*from ZuFang_demo where origin_url=%s""", item['origin_url'])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute("""update ZuFang_demo set city= %s,name= %s,price= %s,way_of_rent= %s,detail= %s,origin_url= %s where origin_url = %s""",
                                        (item['city'],
                                         item['name'],
                                         item['price'],
                                         item['way_of_rent'],
                                         item['detail'],
                                         item['origin_url']
                                         ))
                else:
                    self.cursor.execute(
                        """insert into ZuFang_demo(city, name, price, way_of_rent, detail, origin_url) value(%s, %s, %s, %s, %s, %s)""",
                        (item['city'],
                         item['name'],
                         item['price'],
                         item['way_of_rent'],
                         item['detail'],
                         item['origin_url']
                         ))
                self.connect.commit()
            except Exception as e:
                print(e)
            return item
        elif item.__class__ == ESFHouseItem:
            try:
                self.cursor.execute("""select*from ESFHouse_demo where origin_url=%s""", item['origin_url'])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update ESFHouse_demo set city= %s,title= %s,name= %s,price= %s,unit_price= %s,detail= %s,origin_url= %s where origin_url = %s""",
                        (item['city'],
                         item['title'],
                         item['name'],
                         item['price'],
                         item['unit_price'],
                         item['detail'],
                         item['origin_url']
                         ))
                else:
                    self.cursor.execute(
                        """insert into ESFHouse_demo(city, title, name, unit_price, price, detail, origin_url) value(%s, %s, %s, %s, %s, %s, %s)""",
                        (item['city'],
                         item['title'],
                         item['name'],
                         item['unit_price'],
                         item['price'],
                         item['detail'],
                         item['origin_url']
                         ))
                self.connect.commit()
            except Exception as e:
                print(e)
            return item
        else:
            pass

    def close_spider(self, spider):
        self.connect.close()
