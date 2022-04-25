import beeprint
from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URLS = [
    'https://www.fi.se/sv/publicerat/rapporter/stabilitetsrapporter/',
    'https://www.fi.se/sv/publicerat/rapporter/tillsynsrapporter',
    'https://www.fi.se/sv/publicerat/rapporter/konsumentrapporter/',
    'https://www.fi.se/sv/publicerat/rapporter/bolanerapporter/'
    'https://www.fi.se/sv/publicerat/rapporter/fi-analys/'
    'https://www.fi.se/sv/publicerat/rapporter/rapporter/'
]
INDEX_NAME = 'fi'
URL_RESULT_QUERY_SELECTOR = '.list-item > h2 > a'
NEXT_BTN_QUERY_SELECTOR = '#paging'
DOWNLOAD_BTN_QUERY_SELECTOR = '.link-list * a'


def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = {}
    for url in ROOT_URLS:
        print(f'crawling {url}')
        d = functions.crawl_site(cache_dir, url, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)
        for checksum in d:
            docs[checksum] = d[checksum]

    functions.fetch_titles(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)
    functions.fetch_pdfs(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
