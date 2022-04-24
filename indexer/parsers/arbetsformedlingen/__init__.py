from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URL = 'https://arbetsformedlingen.se/statistik/analyser-och-prognoser'
INDEX_NAME = 'arbetsformedlingen'


def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = functions.crawl_site(cache_dir, ROOT_URL)

    functions.fetch_titles(docs, cache_dir)
    functions.fetch_pdfs(docs, cache_dir)
    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
