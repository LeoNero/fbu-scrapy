import scrapy

class NewsItem(scrapy.Item):
    name = scrapy.Field()
    body_snippet = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
