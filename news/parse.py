import requests
import json
import logging

class Parse(object):
    news_article_path = '/classes/NewsArticle'
    nodes_path = '/classes/Node'

    def __init__(self, app_id, master_key, server_url):
        self.app_id = app_id
        self.master_key = master_key
        self.server_url = server_url
        self.news_article_url = server_url + Parse.news_article_path
        self.nodes_url = server_url + Parse.nodes_path

    def open_connection(self):
        self.__initializeSession()
        self.__setDefaultHeaders()

    def close_connection(self):
        self.session.close()

    def save_item(self, item):
        self.__save_item(item)

    def get_all_nodes(self):
        response = self.session.get(self.nodes_url)
        response_json = response.json()
        return response_json['results']

    def __initializeSession(self):
        self.session = requests.Session()

    def __setDefaultHeaders(self):
        self.session.headers.update({
            'X-Parse-Application-Id': self.app_id,
            'X-Parse-Master-Key': self.master_key,
        })

    def __save_item(self, item):
        news_article = self.__get_news_article_from_item(item)

        if self.__news_article_does_not_exist(news_article):
            self.__save_news_article(news_article)
        else:
            logging.info("Article with url %s already exists in Parse", news_article['Source'])

    def __get_news_article_from_item(self, item):
        return {
            'Name': item['name'],
            'BodySnippet': item['body_snippet'],
            'Body': item['body'],
            'Author': item['author'],
            'Source': item['source'],
            'Image': item['image'],
            'Tags': item['tags']
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