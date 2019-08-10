from functools import reduce
from news.parse import Parse
from news.watson import Watson

class ParsePipeline(object):
    nodes_name_list = []
    nodes_name_id_dict = {}
    word2vec_model = None

    def __init__(self, parse_app_id, parse_master_key, parse_server_url, watson_api_key):
        self.parse = Parse(parse_app_id, parse_master_key, parse_server_url)
        self.watson = Watson(watson_api_key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            parse_app_id=crawler.settings.get('PARSE_APP_ID'),
            parse_master_key=crawler.settings.get('PARSE_MASTER_KEY'),
            parse_server_url=crawler.settings.get('PARSE_SERVER_URL'),
            watson_api_key=crawler.settings.get('WATSON_API_KEY')
        )

    def open_spider(self, spider):
        self.parse.open_connection()

    def close_spider(self, spider):
        self.parse.close_connection()

    def process_item(self, item, spider):
        body_words = self.__get_body_words(item['body'])

        matches = self.__match_body_words_to_nodes(body_words)
        item['tags'] = matches

        self.parse.save_item(item)
        return item

    def __get_body_words(self, body):
        analyze_response = self.watson.analyze_body(body)
        analyze_response_json = analyze_response.json()
        return self.__analyze_response_to_list(analyze_response_json)

    def __analyze_response_to_list(self, analyze_response):
        keywords = analyze_response['keywords']
        entities = analyze_response['entities']
        concepts = analyze_response['concepts']
        categories = analyze_response['categories']

        words_set = set()
        keywords_set = self.__get_set(keywords)
        entities_set = self.__get_set(entities)
        concepts_set = self.__get_set(concepts)
        categories_set = self.__get_categories_set(categories)

        words_set = words_set.union(keywords_set)
        words_set = words_set.union(entities_set)
        words_set = words_set.union(concepts_set)
        words_set = words_set.union(categories_set)

        return list(words_set)

    def __get_set(self, res):
        def clean_words(x, y):
            text = y['text']
            relevance = y['relevance']
            splitted_words = text.split(' ')
            filtered_words = list(filter(None, splitted_words))
            new_words = list(map(lambda x: { 'text': x, 'relevance': relevance }, filtered_words))
            return x + new_words

        words_dict_list = reduce(clean_words, res, [])
        filtered_words = list(filter(lambda x: x['relevance'] >= 0.50, words_dict_list))
        words = set(map(lambda x: x['text'], filtered_words))
        return words

    def __get_categories_set(self, res):
        def clean_categories(x, y):
            label = y['label']
            relevance = y['score']#
            splitted_categories = label.split('/')
            filtered_categories = list(filter(None, splitted_categories))
            new_categories = list(map(lambda x: { 'text': x, 'relevance': relevance }, filtered_categories))
            return x + new_categories

        categories = reduce(clean_categories, res, [])
        return self.__get_set(categories)

    def __match_body_words_to_nodes(self, body_words):
        similar_nodes = set(self.__get_similar_nodes(body_words))
        node_ids = set(map(lambda x: ParsePipeline.nodes_name_id_dict[x], similar_nodes))
        parse_pointers = self.__ids_to_parse_pointers(node_ids)
        return parse_pointers

    def __get_similar_nodes(self, body_words):
        similar_words = []
        for body_word in body_words:
            for node in ParsePipeline.nodes_name_list:
                try:
                    similarity = ParsePipeline.word2vec_model.wv.similarity(w1=body_word, w2=node)
                    if similarity >= 0.40:
                        similar_words.append(node)
                except(KeyError):
                    pass
        return similar_words

    def __ids_to_parse_pointers(self, ids):
        pointers = []
        for object_id in ids:
            pointers.append({
                '__type': 'Pointer',
                'className': 'Node',
                'objectId': object_id
            })
        return pointers