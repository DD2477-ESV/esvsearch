from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URL = 'https://www.msb.se/sv/publikationer/'
INDEX_NAME = 'msb'
URL_RESULT_QUERY_SELECTOR = '.list-item.publication * h2 > a'
NEXT_BTN_QUERY_SELECTOR = '[aria-label="Nästa sida"]'
DOWNLOAD_BTN_QUERY_SELECTOR = '.singellink.tool'


def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = functions.crawl_site(cache_dir, ROOT_URL, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.fetch_titles(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)
    functions.fetch_pdfs(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
