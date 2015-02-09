import datetime

from scrapy.spider import Spider
from scrapy.http import Request

from halalan_scraper.items import ArticleItemLoader

class Philstar(Spider):
  name = 'philstar'
  allowed_domains = ['philstar.com']
  base_url = 'http://www.philstar.com'

  start_urls = ['http://www.philstar.com/nation/archive',
                'http://www.philstar.com/headlines/archive']

  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

  def parse(self, response):
    news_links = response.xpath('//span[@class="article-title"]/a/@href').extract()

    for news in news_links:
      yield Request(url="%s%s" % (self.base_url, news),
        callback=self.extract_article)

    date = response.xpath('//span[@class="date-display-single"]/@content').extract()[0]
    date = date.split('T')[0]
    year = date.split('-')[0]

    if year == '2015':
      next_links = response.xpath('//li[@class="pager-item"]/a/@href').extract()
      next_links = list(set(next_links))

      for next in next_links:
        yield Request(url="%s%s" % (self.base_url, next),
          callback=self.parse)

  def extract_article(self, response):
    date_line = response.xpath('//span[@class="article-date-info"]/text()').extract()[0]
    date = date_line.split(' - ')[0].replace('Updated ', '').replace(',', '').split()
    year = date[-1]
    month = date[0]
    day = date[1]
    date = datetime.date(int(year), self.months.index(month) + 1, int(day)).isoformat()

    if year == '2015':
      url = response.url

      loader = ArticleItemLoader()

      title = response.xpath('id("page-title")/text()').extract()[0]
      title = title.replace('\n', '').strip()
      article_id = url.split('/')[-2]
      article_id = "philstar-%s" % article_id

      article = response.xpath('//div[@class="field-item even"]/p/text()').extract()
      article = "\n".join(article)

      if article == '':
        article = response.xpath('//div[@class="field-item even"]/div/text()[normalize-space()]').extract()
        article = "\n".join(article)

      loader.add_value('title', title)
      loader.add_value('url', url)
      loader.add_value('article_id', article_id)
      loader.add_value('article', article)
      loader.add_value('date', date)

      yield loader.load_item()