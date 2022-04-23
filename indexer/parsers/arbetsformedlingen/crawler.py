import time
import urllib
import pathlib
from . import console
from . import browser
from . import document


class Crawler:

    def __init__(self, cache_dir) -> None:
        self.browser = None
        self.cache_dir = cache_dir
        self.documents = {}

    async def start_browser(self):
        self.browser = browser.Browser()
        await self.browser.start()

    async def route_to(self, url):
        await self.browser.page.goto(url)

    async def add_urls_from_current_page(self):
        found_new_links = False

        elements = await self.browser.page.querySelectorAll('.af-report-result__item * a')
        for element in elements:
            href = await self.browser.page.evaluate('(element) => element.href', element)
            doc = document.Doc(href)

            if doc.checksum not in self.documents:
                found_new_links = True

            self.documents[doc.checksum] = doc

        return found_new_links

    async def next_page_and_wait(self):
        btn = await self.browser.page.querySelector('[aria-label="Nästa sida"]')
        await btn.click()
        time.sleep(1)

    async def crawl(self, root_url):
        await self.route_to(root_url)
        await self.add_urls_from_current_page()

        console.log('crawling src', end='')
        while True:
            console.log('.', end='')
            await self.next_page_and_wait()
            found_new_links = await self.add_urls_from_current_page()
            if not found_new_links:
                break
        console.log('done.')

    async def crawl_for_title(self, doc: document.Doc):
        cache_filename = f'{self.cache_dir}/titles/{doc.checksum}.txt'
        if pathlib.Path(cache_filename).exists():
            with open(cache_filename, 'r') as file:
                doc.title = file.read().strip()
                return

        await self.browser.page.goto(doc.url)

        title = await self.browser.page.title()
        doc.title = title

        with open(cache_filename, 'w') as out:
            out.write(title)

    async def crawl_for_download(self, doc: document.Doc):
        download_url_filename = f'{self.cache_dir}/download_urls/{doc.checksum}.txt'
        if pathlib.Path(download_url_filename).exists():
            with open(download_url_filename, 'r') as file:
                doc.download_url = file.read().strip()
                return

        await self.browser.page.goto(doc.url)

        element = await self.browser.page.querySelector('[download]')
        if element is None:
            return

        url = await self.browser.page.evaluate('(element) => element.href', element)
        doc.download_url = url

        with open(download_url_filename, 'w') as out:
            out.write(doc.download_url)
