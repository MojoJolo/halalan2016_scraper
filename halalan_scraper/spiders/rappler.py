from scrapy.spider import Spider
from scrapy.http import Request

from halalan_scraper.items import ArticleItemLoader

class Rappler(Spider):
  name = 'rappler'
  allowed_domains = ['rappler.com']
  base_url = 'http://www.rappler.com'

  start_urls = ['http://www.rappler.com/previous-articles?filterCategory54d0eb581a5b6_1=21&filterCategory=21&filterCategory54d0eb581a5b6_2=21&filterTitle=&filterMeta=&filterDateFrom=2015-01-01&filterDateTo=&option=com_dmarticlesfilter&view=articles&Itemid=1404&userSearch=1']

  def parse(self, response):
    news_links = response.xpath('//h4/a/@href').extract()

    for news in news_links:
      yield Request(url="%s%s" % (self.base_url, news),
        callback=self.extract_article)

    # next_links = response.xpath('//a[@class="pagenav" and @title="Next"]/@href').extract()
    next_links = response.xpath('//a[@class="pagenav"]/@href').extract()
    next_links = list(set(next_links))

    for next in next_links:
      yield Request(url="%s%s" % (self.base_url, next),
        callback=self.parse)

  def extract_article(self, response):
    url = response.url

    loader = ArticleItemLoader()

    title = response.xpath('//h1/text()').extract()
    article_id = url.split('/')[-1].split('-')[0]
    article_id = "rappler-%s" % article_id

    article = response.xpath('//div[@class="storypage-divider"]/p/text()').extract()
    article = "\n".join(article)

    loader.add_value('title', title)
    loader.add_value('url', url)
    loader.add_value('article_id', article_id)
    loader.add_value('article', article)

    yield loader.load_item()
