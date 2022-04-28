import beeprint
from ..crawler import functions
from ..constants import ELASTICSEARCH_ENDPOINT


ROOT_URLS = [
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/broschyrer-om-riksbanken/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/publikationer-fran-ecb/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ekonomiska-kommentarer/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/finansmarknadsenkat/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/foretagsundersokning/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/penning--och-valutapolitik/artiklar-i-penning--och-valutapolitik/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/penning--och-valutapolitik/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/redogorelse-for-penningpolitiken/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/riksbanksstudier/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/staff-memo/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/working-paper-series/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/arsredovisning/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ovriga-tidigare-utgivna-publikationer/den-svenska-finansmarknaden/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ovriga-tidigare-utgivna-publikationer/emu-skrifter/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ovriga-tidigare-utgivna-publikationer/finansiell-infrastruktur/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ovriga-tidigare-utgivna-publikationer/riksbanken-och-finansiell-stabilitet/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ovriga-tidigare-utgivna-publikationer/sedel--och-myntskrifter/',
    'https://www.riksbank.se/sv/press-och-publicerat/publikationer/ovriga-tidigare-utgivna-publikationer/riskenkat/',
]
INDEX_NAME = 'riksbanken'
URL_RESULT_QUERY_SELECTOR = '.listing-block__body * li > a'
NEXT_BTN_QUERY_SELECTOR = None
DOWNLOAD_BTN_QUERY_SELECTOR = None


def parse(args):
    cache_dir = args.src

    functions.create_cache_dir(cache_dir)

    docs = {}
    for url in ROOT_URLS:
        print(f'crawling {url}')
        d = functions.crawl_site(cache_dir, url, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)
        for checksum in d:
            docs[checksum] = d[checksum]

    functions.fetch_pdfs(docs, cache_dir, URL_RESULT_QUERY_SELECTOR, NEXT_BTN_QUERY_SELECTOR, DOWNLOAD_BTN_QUERY_SELECTOR)

    functions.parse_titles_from_pdf(docs, cache_dir)
    functions.parse_text(docs, cache_dir)
    functions.parse_dates(docs, cache_dir)
    functions.index_documents(docs, cache_dir, ELASTICSEARCH_ENDPOINT, INDEX_NAME)
