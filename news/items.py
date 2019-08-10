import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose

def clean_url(value):
    if value != None and value != '':
        return value[2:]
    return value

class NewsItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    body_snippet = scrapy.Field(output_processor=Join())
    body = scrapy.Field(output_processor=Join())
    author = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field(
        input_processor=MapCompose(clean_url),
        output_processor=TakeFirst()
    )
    tags = scrapy.Field()
