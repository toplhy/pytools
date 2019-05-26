# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from biquge import settings


class BiqugePipeline(object):

    def __init__(self):
        db = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DBNAME,
            charset=settings.MYSQL_CHARSET
        )
        self.db = db
        self.cursor = db.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("select count(1) from books where id = %s" % (item["book_id"]))
            book_count = self.cursor.fetchone()[0]
            if book_count == 0:
                book_insert_sql = "insert into books(id, name, author, type, url) values('{0}', '{1}', '{2}', '{3}', '{4}')"
                self.cursor.execute(book_insert_sql.format(item["book_id"], item["book_name"], item["book_author"], item["book_type"], item["book_url"]))
            chapter_insert_sql = "insert into chapters(name, sortNum, url, content, books_id) values('{0}', '{1}', '{2}', '{3}', '{4}')"
            self.cursor.execute(chapter_insert_sql.format(item["chapter_name"], item["chapter_num"], item["chapter_url"], item["chapter_content"], item["book_id"]))
            self.db.commit()
        except:
            print("Error: unable to fetch data")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
