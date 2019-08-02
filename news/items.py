import scrapy
from scrapy.loader.processors import TakeFirst, Join

class NewsItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    body_snippet = scrapy.Field(output_processor=Join())
    body = scrapy.Field(output_processor=Join())
    author = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())
