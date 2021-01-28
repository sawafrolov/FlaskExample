from requests import get, ConnectionError
from elasticsearch import Elasticsearch


def check_elasticsearch(url):
    try:
        response = get(url).json()
    except ConnectionError:
        return False
    if "cluster_name" in response:
        if response["cluster_name"] == "elasticsearch":
            return True
    return False


def enable_elasticsearch(url):
    if check_elasticsearch(url):
        return Elasticsearch([url])
    return None
