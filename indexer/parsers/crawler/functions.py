import sys
import asyncio
import beeprint
from . import cache
from . import console
from . import crawler
from . import index_definitions
from rich.progress import Progress
from elasticsearch import Elasticsearch


def create_cache_dir(cache_dir):
    console.log(f'using cache dir at {cache_dir}')
    cache.create_cache(cache_dir)


def crawl_site(
    cache_dir,
    root_url,
    url_result_query_selector,
    next_btn_query_selector,
    download_btn_query_selector
):
    console.log('fetching docs')
    c = crawler.Crawler(
        cache_dir,
        url_result_query_selector,
        next_btn_query_selector,
        download_btn_query_selector
    )

    asyncio.get_event_loop().run_until_complete(c.start_browser())
    asyncio.get_event_loop().run_until_complete(c.crawl(root_url))

    console.log(f'found {len(c.documents)} docs')
    return c.documents


def fetch_titles(
    docs,
    cache_dir,
    url_result_query_selector,
    next_btn_query_selector,
    download_btn_query_selector
):
    c = crawler.Crawler(
        cache_dir,
        url_result_query_selector,
        next_btn_query_selector,
        download_btn_query_selector
    )
    asyncio.get_event_loop().run_until_complete(c.start_browser())

    with Progress() as progress:
        task1 = progress.add_task('Fetching titles...', total=len(docs))

        for checksum in docs:
            doc = docs[checksum]
            asyncio.get_event_loop().run_until_complete(c.crawl_for_title(doc))
            progress.update(task1, advance=1)


def fetch_pdfs(
    docs,
    cache_dir,
    url_result_query_selector,
    next_btn_query_selector,
    download_btn_query_selector
):
    c = crawler.Crawler(
        cache_dir,
        url_result_query_selector,
        next_btn_query_selector,
        download_btn_query_selector
    )
    asyncio.get_event_loop().run_until_complete(c.start_browser())

    with Progress() as progress:
        task1 = progress.add_task('Fetching PDFs...', total=len(docs))

        for checksum in docs:
            doc = docs[checksum]
            try:
                asyncio.get_event_loop().run_until_complete(c.crawl_for_download(doc))
            except Exception as e:
                progress.update(task1, advance=1)
                continue

            if doc.is_downloaded(cache_dir):
                progress.update(task1, advance=1)
                continue

            doc.download(cache_dir)
            progress.update(task1, advance=1)


def parse_text(docs, cache_dir):
    with Progress() as progress:
        task1 = progress.add_task('Parsing Text...', total=len(docs))

        for checksum in docs:
            doc = docs[checksum]
            doc.parse_text(cache_dir)
            progress.update(task1, advance=1)


def parse_dates(docs, cache_dir):
    with Progress() as progress:
        task1 = progress.add_task('Parsing Dates...', total=len(docs))

        for checksum in docs:
            doc = docs[checksum]
            doc.parse_dates(cache_dir)
            progress.update(task1, advance=1)


def parse_titles_from_pdf(docs, cache_dir):
    with Progress() as progress:
        task1 = progress.add_task('Parsing Titles from PDFS...', total=len(docs))

        for checksum in docs:
            doc = docs[checksum]
            doc.parse_title(cache_dir)
            progress.update(task1, advance=1)


def index_documents(docs, cache_dir, endpoint, index_name):
    es = Elasticsearch(endpoint)
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        console.log(f'Index: {index_name} already exists. Would you like to delete, append, or abort')
        answer = input('Type one of [O]verwrite, [A]ppend or [C]ancel: ')
        if answer.lower() == 'o':
            es.indices.delete(index=index_name, ignore=[400, 404])
            index_exists = False
        elif answer.lower() == 'c':
            sys.exit(0)

    if not index_exists:
        request_body = {
            'settings': index_definitions.INDEX_SETTINGS,
            'mappings': index_definitions.INDEX_MAPPINGS
        }
        es.indices.create(index=index_name, body=request_body)

    for checksum in docs:
        doc = docs[checksum]
        es.index(
            index=index_name,
            id=doc.checksum,
            body=doc.to_dict()
        )
