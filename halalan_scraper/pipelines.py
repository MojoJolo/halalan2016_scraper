# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db import Db

class HalalanScraperPipeline(object):
  def process_item(self, item, spider):
    return item


class MySQLStorePipeline(object):
  def process_item(self, item, spider):
    if not Db().isExisting(item['article_id']):
      Db().insert(item)

      return item
    else:
      pass