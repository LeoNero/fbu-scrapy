from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news.parse import Parse
from news.pipelines import ParsePipeline
import gensim
import sys

nodes_name_list = []
nodes_name_id_dict = {}

def get_name(node):
    return node['name']

def nodes_to_name_id_dict(nodes):
    nodes_dict = {}
    for node in nodes:
        node_name = node['name']
        node_id = node['objectId']
        nodes_dict[node_name] = node_id
    return nodes_dict

def main():
    settings = get_project_settings()
    settings.set('WATSON_API_KEY', sys.argv[1], 40)

    parse_server_url = settings["PARSE_SERVER_URL"]
    parse_app_id = settings["PARSE_APP_ID"]
    parse_master_key = settings["PARSE_MASTER_KEY"]

    parse = Parse(parse_app_id, parse_master_key, parse_server_url)
    parse.open_connection()

    nodes = parse.get_all_nodes()

    nodes_name_list = list(map(get_name, nodes))
    nodes_name_id_dict = nodes_to_name_id_dict(nodes)

    print("TRAINING WORD2VEC MODEL...")
    #word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
    #word2vec_model.save('fbu')
    word2vec_model = gensim.models.KeyedVectors.load('fbu', mmap='r')

    ParsePipeline.nodes_name_list = nodes_name_list
    ParsePipeline.nodes_name_id_dict = nodes_name_id_dict
    ParsePipeline.word2vec_model = word2vec_model

    parse.close_connection()

    process = CrawlerProcess(settings)
    process.crawl('cnn')
    process.start()

main()