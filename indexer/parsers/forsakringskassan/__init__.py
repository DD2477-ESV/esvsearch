from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URL = 'https://www.forsakringskassan.se/statistik/publikationer#/'
INDEX_NAME = 'forsakringskassan'
URL_RESULT_QUERY_SELECTOR = 'h3 > a'
NEXT_BTN_QUERY_SELECTOR = '#publikationer > button'
DOWNLOAD_BTN_QUERY_SELECTOR = None


def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = functions.crawl_site(cache_dir, ROOT_URL, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.fetch_pdfs(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)
    functions.parse_titles_from_pdf(docs, cache_dir)

    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
