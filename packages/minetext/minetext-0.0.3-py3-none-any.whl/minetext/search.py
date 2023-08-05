from minetext.ElasticsearchUtils import ElasticsearchUtils


def search(term: str):
    print(f'Search with term: {term}')
    es = ElasticsearchUtils()
    print(es.search(term))


def download_files():
    print('Download files...')
