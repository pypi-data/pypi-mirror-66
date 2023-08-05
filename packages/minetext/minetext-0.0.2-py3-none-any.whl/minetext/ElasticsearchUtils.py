from elasticsearch import Elasticsearch


class ElasticsearchUtils:
    """
    This class provides all necessary functions to interact with Elasticsearch
    """

    def __init__(self):
        self._es = Elasticsearch('http://141.5.110.132:9200')

    def search(self, term: str):
        search_body = {
            'query': {
                'query_string': {
                    'query': term
                }
            }
        }
        return self._es.search(index='goescholar', body=search_body)


if __name__ == '__main__':
    es = ElasticsearchUtils()
    print(es.search('text'))
