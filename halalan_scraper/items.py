# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst


class ArticleItem(Item):
  article_id = Field()
  url = Field()
  title = Field()
  article = Field()
  date = Field() # 2015-02-05 ISO format

class ArticleItemLoader(ItemLoader):
  default_item_class = ArticleItem
  default_input_processor = Identity()
  default_output_processor = TakeFirst()