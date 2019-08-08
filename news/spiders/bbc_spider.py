import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem

class BBCSpider(CrawlSpider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]
    start_urls = [
        "https://www.bbc.com/news"
    ]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        news = ItemLoader(item=NewsItem(), response=response)

        if response.css('h1.story-body__h1::text').get() != None:
            news.add_css('name', 'h1.story-body__h1::text')
        elif response.css('.story-body__h1::text').get() != None:
            news.add_css('name', '.story-body__h1::text')
        else:
            return

        news.add_value('author', 'BBC')

        if response.css('.js-image-replace::attr(src)').get() != None:
            news.add_css('image', '.js-image-replace::attr(src)')
        else:
            return

        if response.css('.story-body__introduction::text').get() != None:
            news.add_css('body_snippet', '.story-body__introduction::text')
        elif response.css('div.story-body__inner p::text').get() != None:
            news.add_css('body_snippet', "div.story-body__inner p::text")
        else:
            return

        if response.css('.story-body p::text').get() != None:
            news.add_css('body', '.story-body p::text')
        else:
            return

        news.add_value('source', response.url)
        return news.load_item()
