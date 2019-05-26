# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    book_type = scrapy.Field()
    book_author = scrapy.Field()
    book_url = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_num = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_content = scrapy.Field()
    pass
