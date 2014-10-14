# -*- coding: utf-8 -*-
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KhanClassesItem(scrapy.Item):
    domain = scrapy.Field()
    subject = scrapy.Field()
    lesson = scrapy.Field()
    image = scrapy.Field()
    pass