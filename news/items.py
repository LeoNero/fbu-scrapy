import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose

def clean_url(value):
    if value != None and value != '':
        splitted_url = value.split('//')
        protocol = splitted_url[0]

        if protocol == '':
            return 'https:' + value

        if len(splitted_url) == 1:
          return 'https://' + value

        if protocol != 'https:' or protocol != 'http:':
            return value

        return 'https://' + value
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
