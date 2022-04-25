import time
import urllib
import pathlib
from . import console
from . import browser
from . import document


NEXT_BUTTON_CLICK_LIMIT = 1000


class Crawler:

    def __init__(
        self,
        cache_dir,
        url_result_query_selector,
        next_btn_query_selector,
        download_btn_query_selector,
    ) -> None:
        self.browser = None
        self.cache_dir = cache_dir
        self.documents = {}
        self.url_result_query_selector = url_result_query_selector
        self.next_btn_query_selector = next_btn_query_selector
        self.download_btn_query_selector = download_btn_query_selector

    async def start_browser(self):
        self.browser = browser.Browser()
        await self.browser.start()

    async def route_to(self, url):
        await self.browser.page.goto(url)
        time.sleep(.1)

    async def press_button(self, query_selector):
        btn = await self.browser.page.querySelector(query_selector)
        time.sleep(.1)

        try:
            await btn.click()
            time.sleep(2)
        except Exception as e:
            print(e)

    async def add_urls_from_current_page(self):
        found_new_links = False

        try:
            await self.browser.page.waitForSelector(self.url_result_query_selector, timeout=2000)
        except Exception as e:
            print(e)
            return

        elements = await self.browser.page.querySelectorAll(self.url_result_query_selector)

        for element in elements:
            href = await self.browser.page.evaluate('(element) => element.href', element)
            doc = document.Doc(href)

            if doc.checksum not in self.documents:
                found_new_links = True

            self.documents[doc.checksum] = doc

        return found_new_links

    async def next_page_and_wait(self):
        btn = None
        max_wait = 20
        waited = 0
        while btn is None:
            waited += 1
            if waited > max_wait:
                return
            btn = await self.browser.page.querySelector(self.next_btn_query_selector)
            time.sleep(.1)

        try:
            await btn.click()
            time.sleep(2)
        except Exception as e:
            print(e)

    async def crawl(self, root_url):
        await self.route_to(root_url)
        await self.add_urls_from_current_page()

        console.log('crawling src', end='')
        pages = 0
        while True:
            console.log('.', end='')
            pages += 1
            if pages > NEXT_BUTTON_CLICK_LIMIT:
                break

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

        try:
            await self.browser.page.goto(doc.url, waitUntil='networkidle2')
            await self.browser.page.waitForSelector('title', timeout=2000)

            title = await self.browser.page.title()
            doc.title = title

            with open(cache_filename, 'w') as out:
                out.write(title)
        except Exception as e:
            print(e)
            doc.title = ''

    async def crawl_for_download(self, doc: document.Doc):
        download_url_filename = f'{self.cache_dir}/download_urls/{doc.checksum}.txt'
        if pathlib.Path(download_url_filename).exists():
            with open(download_url_filename, 'r') as file:
                doc.download_url = file.read().strip()
                return

        if self.download_btn_query_selector is None:
            # the doc.url is also the download_url
            doc.download_url = doc.url
        else:
            await self.browser.page.goto(doc.url)

            element = await self.browser.page.querySelector(self.download_btn_query_selector)
            if element is None:
                return

            url = await self.browser.page.evaluate('(element) => element.href', element)
            doc.download_url = url

        with open(download_url_filename, 'w') as out:
            out.write(doc.download_url)
