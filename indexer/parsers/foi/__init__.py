from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URL = 'https://www.foi.se/rapporter.html'
INDEX_NAME = 'foi'
URL_RESULT_QUERY_SELECTOR = '.foi-report__title > a'
NEXT_BTN_QUERY_SELECTOR = '.pagination > li.page-item:last-child > a'
DOWNLOAD_BTN_QUERY_SELECTOR = '.foi-report__save-button'
BTN_PRESS_AFTER_LOADING_QUERY_SELECTOR = '.foi-report-search * .input-group-append > button'

def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = functions.crawl_site(
        cache_dir,
        ROOT_URL,
        URL_RESULT_QUERY_SELECTOR,
        NEXT_BTN_QUERY_SELECTOR,
        DOWNLOAD_BTN_QUERY_SELECTOR,
        BTN_PRESS_AFTER_LOADING_QUERY_SELECTOR
    )

    functions.fetch_pdfs(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.parse_titles_from_pdf(docs, cache_dir)
    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
