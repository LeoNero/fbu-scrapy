import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem

class CnnSpider(CrawlSpider):
    name = "cnn"
    allowed_domains = ["www.cnn.com"]
    start_urls = [
        "https://www.cnn.com/"
    ]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        splitted_url = response.url.split('/')

        if (len(splitted_url) < 4):
            return

        if (splitted_url[3] != '2019'):
            return

        news = ItemLoader(item=NewsItem(), response=response)
        news.add_css('name', 'h1.pg-headline::text')

        if response.css('span.metadata__byline__author a::text').get() == None:
            news.add_css('author', 'span.metadata__byline__author::text')
        else:
            news.add_css('author', 'span.metadata__byline__author a::text')

        if response.css('.media__image::attr(data-src-medium)').get() != None:
            news.add_css('image', '.media__image::attr(data-src-medium)')

        news.add_css('body_snippet', '.zn-body__paragraph.speakable *::text')
        news.add_css('body', '.zn-body__paragraph *::text')
        news.add_value('source', response.url)

        return news.load_item()
