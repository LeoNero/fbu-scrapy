import requests
import json
import logging

class ParsePipeline(object):
    news_article_path = '/classes/NewsArticle'

    def __init__(self, app_id, master_key, server_url):
        self.app_id = app_id
        self.master_key = master_key
        self.server_url = server_url
        self.news_article_url = self.server_url + ParsePipeline.news_article_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            app_id=crawler.settings.get('PARSE_APP_ID'),
            master_key=crawler.settings.get('PARSE_MASTER_KEY'),
            server_url=crawler.settings.get('PARSE_SERVER_URL')
        )

    def open_spider(self, spider):
        self.__initializeSession()
        self.__setDefaultHeaders()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        self.__save_item(item)
        return item

    def __initializeSession(self):
        self.session = requests.Session()

    def __setDefaultHeaders(self):
        self.session.headers.update({
            'X-Parse-Application-Id': 'LeoHaleyPlaxides',
            'X-Parse-Master-Key': 'LeoHaleyPlaxides'
        })

    def __save_item(self, item):
        news_article = self.__get_news_article_from_item(item)

        if self.__news_article_does_not_exist(news_article):
            self.__save_news_article(news_article)
        else:
            logging.info("Article with url %s already exists in Parse", news_article['Source'])

    def __get_news_article_from_item(self, item):
        return {
            'Name': item['name'][0],
            'BodySnippet': item['body_snippet'][0],
            'Body': item['body'][0],
            'Author': item['author'][0],
            'Source': item['source'][0]
        }

    def __news_article_does_not_exist(self, news_article):
        source = news_article['Source']
        params = self.__find_article_by_source_params(source)
        response = self.session.get(
            self.news_article_url,
            params=params
        )
        json_response = response.json()
        results = json_response['results']
        results_size = len(results)

        return results_size == 0

    def __save_news_article(self, news_article):
        save_response = self.session.post(
            self.news_article_url,
            json=news_article
        )
        self.__handle_save_response(save_response, news_article)

    def __find_article_by_source_params(self, source):
        return {
            'where': json.dumps({
                'Source': {
                    '$in': [source]
                }
            })
        }

    def __handle_save_response(self, save_response, news_article):
        save_response_json = save_response.json()
        if save_response.status_code == 201:
            logging.info(
                "Article with url %s saved, and has id %s :)",
                news_article['Source'],
                save_response_json['objectId']
            )
        else:
            logging.error("Article with url %s not saved :( or response was not the expected", news_article['Source'])
            logging.error(save_response_json)
