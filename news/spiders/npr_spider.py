import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem

class NprSpider(CrawlSpider):
    name = "npr"
    allowed_domains = ["www.npr.org"]
    start_urls = [
        "https://www.npr.org"
    ]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        news = ItemLoader(item=NewsItem(), response=response)

        if response.css('div.storytitle h1::text').get() == None:
            return
        else:
            news.add_css('name', 'div.storytitle h1::text')

        if response.css('p.byline__name a::attr(href)').get() == None:
            return
        else:
                news.add_css('author', 'p.byline__name a::attr(href)')

        if response.css('.imagewrap img::attr(src)').get() == None:
            return
        else:
            news.add_css('image', '.imagewrap img::attr(src)')

        if response.css('div.storytext p::text').get() == None:
            return
        else:
              news.add_css('body_snippet', 'div.storytext p::text')

        if response.css('div.storytext p::text').get() == None:
            return
        else:
            news.add_css('body', 'div.storytext p::text')

        news.add_value('source', response.url)

        return news.load_item()
