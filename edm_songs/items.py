# -*- coding: utf-8 -*-
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EdmSongsItem(scrapy.Item):
    title = scrapy.Field()
    artist = scrapy.Field()
    link = scrapy.Field()
    notes = scrapy.Field()
    postAuthor = scrapy.Field()
    postDate = scrapy.Field()
    pass
