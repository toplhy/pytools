# -*- coding: utf-8 -*-
import scrapy

from biquge.items import BiqugeItem


class BqgSpider(scrapy.Spider):
    name = 'bqg'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['http://www.xbiquge.la/xiaoshuodaquan/', ]

    def parse(self, response):
        for index, book_url in enumerate(response.xpath("//div[@class='novellist']/ul/li/a/@href").extract()):
            request = scrapy.Request(url=book_url, callback=self.parse_chapter)
            request.meta["book_id"] = (index + 1)
            yield request

    def parse_chapter(self, response):
        book_id = response.meta["book_id"]
        for index, chapter in enumerate(response.xpath("//dd")):
            item = BiqugeItem()
            item["book_id"] = book_id
            item["book_name"] = response.xpath("//*[@id='info']/h1/text()").extract()[0]
            item["book_type"] = response.xpath("//*[@class='con_top']/a[2]/text()").extract()[0]
            author = response.xpath("//*[@id='info']/p[1]/text()").extract()[0]
            item["book_author"] = author[7:]
            item["book_url"] = response.url
            item["chapter_name"] = chapter.xpath("./a/text()").extract()[0]
            item["chapter_num"] = (index + 1)
            item["chapter_url"] = "http://www.xbiquge.la%s" % (chapter.xpath("./a/@href").extract())[0]
            request = scrapy.Request(url=item["chapter_url"], callback=self.parse_content)
            request.meta["item"] = item
            yield request

    def parse_content(self, response):
        item = response.meta["item"]
        item["chapter_content"] = str(response.xpath("//*[@id='content']").extract())[2:-2]
        yield item
