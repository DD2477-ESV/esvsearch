INDEX_SETTINGS = {
    'index': {
        'refresh_interval': '1s',
        'number_of_shards': 1,
        'number_of_replicas': 0,
        'highlight.max_analyzed_offset': 15000000,
    },
    "analysis": {
        "analyzer": {
            "my_custom_analyzer": {
                "tokenizer": "standard",
                "char_filter": [
                    "replace_dot_html_with_dash_html"
                ],
                "filter": ["lowercase", "swedish_stemmer"]
            }
        },
        "filter": {
            "swedish_stemmer": {
                "type": "stemmer",
                "name": "swedish"
            }
        },
        "char_filter": {
            "replace_dot_html_with_dash_html": {
                "type": "mapping",
                "mappings": [
                    ".html => -html"
                ]
            }
        }
    }
}

INDEX_MAPPINGS = {
    'properties': {
        "content": {
            "type": "text",
            "analyzer": "my_custom_analyzer",
        },
        "relative_path_to_file": {
            "type": "text",
            "analyzer": "my_custom_analyzer",
            "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            }
        },
        "title": {
            "type": "text",
            "analyzer": "my_custom_analyzer",
            "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            }
        }
    }
}
