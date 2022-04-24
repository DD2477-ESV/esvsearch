from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URL = 'https://www.esv.se/publicerat/publikationer/Search/'
INDEX_NAME = 'esv'
URL_RESULT_QUERY_SELECTOR = '[search-hit-activator]'
NEXT_BTN_QUERY_SELECTOR = 'button.arrow_blue'
DOWNLOAD_BTN_QUERY_SELECTOR = '.ga_publication'


def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = functions.crawl_site(cache_dir, ROOT_URL, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.fetch_titles(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)
    functions.fetch_pdfs(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
