import datetime

from scrapy.spider import Spider
from scrapy.http import Request

from halalan_scraper.items import ArticleItemLoader

class Inquirer(Spider):
  name = 'inquirer'
  allowed_domains = ['newsinfo.inquirer.net']

  start_urls = ['http://newsinfo.inquirer.net/category/latest-stories']

  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

  def parse(self, response):
    news_links = response.xpath('//div[@class="ncatstories"]/a[position() mod 2 = 0]/@href').extract()

    for news in news_links:
      yield Request(url=news,
        callback=self.extract_article)

    date = response.xpath('//div[@class="time"]/text()').extract()[0]
    year = date.split()[-1]

    if year == '2015':
      next_link = response.xpath('//div[@class="cal-nav"]/a/@href').extract()

      if len(next_link) > 1:
        next_link = next_link[1]
      else:
        next_link = next_link[0]

      yield Request(url=next_link, callback=self.parse)

  def extract_article(self, response):
    byline = response.xpath('//h4[@class="byline"]/text()').extract()

    if len(byline) > 1:
      byline = byline[-1]
    else:
      byline = byline[0]

    date = byline.split(' | ')[-1]
    date = date.replace(',', '').split()[1:]
    month = date[0]
    day = date[1].replace('th', '').replace('nd', '').replace('st', '').replace('rd', '')
    year = date[-1]
    date = datetime.date(int(year), self.months.index(month) + 1, int(day)).isoformat()

    if year == '2015':
      url = response.url

      loader = ArticleItemLoader()

      title = response.xpath('//h1/text()').extract()
      article_id = url.split('/')[-2]
      article_id = "inquirer-%s" % article_id

      article = response.xpath('//div[@class="main-article"]/p/text()').extract()
      article = "\n".join(article)

      loader.add_value('title', title)
      loader.add_value('url', url)
      loader.add_value('article_id', article_id)
      loader.add_value('article', article)
      loader.add_value('date', date)

      yield loader.load_item()