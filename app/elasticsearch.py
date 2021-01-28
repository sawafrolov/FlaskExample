from elasticsearch import Elasticsearch


def check_elasticsearch(url):
    return False


def enable_elasticsearch(url):
    if check_elasticsearch(url):
        return Elasticsearch([url])
    return None
