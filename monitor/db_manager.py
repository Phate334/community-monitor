from datetime import datetime, timedelta

import meilisearch

from monitor.config import get_settings

settings = get_settings()
client = meilisearch.Client(settings.meilisearch_url, settings.meilisearch_api_key)


def query(index_name: str):
    index = client.index(index_name)
    return index.search("", {"sort": ["published:desc"], "limit": 1})


def cleanup_index(index_name: str):
    index = client.index(index_name)
    index.delete()


def create_index(index_name: str):
    index = client.index(index_name)
    index_settings = {
        "filterableAttributes": ["published"],
        "sortableAttributes": ["published"],
    }
    index.update(primary_key="id")
    index.update_settings(index_settings)


if __name__ == "__main__":
    res = query("arxiv")
    print(res)
