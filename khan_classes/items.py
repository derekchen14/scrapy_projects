# -*- coding: utf-8 -*-
import scrapy

class KhanClassesItem(scrapy.Item):
    subject = scrapy.Field()
    domain = scrapy.Field()
    lesson = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
