INDEX_SETTINGS = {
    'index': {
        'refresh_interval': '1s',
        'number_of_shards': 1,
        'number_of_replicas': 0,
    },
    'analysis': {
        'analyzer': {
            'my_custom_analyzer': {
                'tokenizer': 'standard',
                'char_filter': [
                    'replace_dot_html_with_dash_html'
                ],
                'filter': ['lowercase', 'swedish_stemmer']
            }
        },
        'filter': {
            'swedish_stemmer': {
                'type': 'stemmer',
                'name': 'swedish'
            }
        },
        'char_filter': {
            'replace_dot_html_with_dash_html': {
                'type': 'mapping',
                'mappings': [
                    '.html => -html'
                ]
            }
        }
    }
}

INDEX_MAPPINGS = {
    'properties': {
        'text': {
            'type': 'text',
            'analyzer': 'my_custom_analyzer',
        },
        'date': {
            'type': 'date',
            'ignore_malformed': True,
        },
        'title': {
            'type': 'text',
            'analyzer': 'my_custom_analyzer',
            'fields': {
                'keyword': {
                    'type': 'keyword',
                    'ignore_above': 256
                }
            }
        },
        'url': {
            'type': 'text',
        }
    }
}
