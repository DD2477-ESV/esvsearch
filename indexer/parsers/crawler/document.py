import hashlib
import pathlib
import certifi
import requests
from . import dates
from . import console
from PyPDF2 import PdfFileReader
from dateutil.parser import parse
from pdfminer.high_level import extract_text
from requests.packages.urllib3.exceptions import InsecureRequestWarning


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0'


class Doc:

    def __init__(
        self,
        url: str,
        download_url: str = None,
        text: str = None,
        date: str = None,
        title: str = None,
    ) -> None:
        self.url = url
        self.download_url = download_url
        self.checksum = hashlib.sha256(url.encode('utf-8')).hexdigest()
        self.date = date
        self.text = text
        self.title = title

    def to_dict(self) -> dict:
        date = None
        if self.date is not None:
            if self.date.strip() != '':
                date = parse(self.date)
        return {
            'url': self.url,
            'download_url': self.download_url,
            'date': date,
            'text': self.text,
            'title': self.title,
        }

    def is_downloaded(self, cache_dir: str) -> bool:
        return pathlib.Path(f'{cache_dir}/pdfs/{self.checksum}.pdf').exists()

    def download(self, cache_dir: str) -> bool:
        output_filename = f'{cache_dir}/pdfs/{self.checksum}.pdf'

        if self.download_url is None:
            return

        # For some reason my python installation is having a real fuzz with the
        # ssl certificate trust validation. Disabling ssl verification is obviously
        # super bad practice. But i've spent hours recompiling my python install
        # and it's just not working, so disabling ssl. This is just a uni project
        # soooo i don't care :)
        should_verify = False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        try:
            headers = {'User-Agent': USER_AGENT}
            with requests.get(
                self.download_url,
                stream=True,
                headers=headers,
                verify=should_verify,
            ) as r:
                r.raise_for_status()
                with open(output_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except requests.exceptions.HTTPError:
            pass

    def parse_text(self, cache_dir: str) -> bool:
        input = f'{cache_dir}/pdfs/{self.checksum}.pdf'
        output = f'{cache_dir}/text/{self.checksum}.txt'
        if not pathlib.Path(input).exists():
            return

        if pathlib.Path(output).exists():
            with open(output, 'r') as src:
                self.text = src.read().strip()
            return

        try:
            print(f'parsing text in {self.checksum}')
            with open(input, 'rb') as src:
                text = extract_text(
                    src,
                    password='',
                    page_numbers=None,
                    maxpages=0,
                    caching=True,
                    codec='utf-8',
                    laparams=None
                )
                with open(output, 'w') as out:
                    out.write(text)
                self.text = text
        except Exception as e:
            print(e)
            self.text = 'parse error'

    def parse_dates(self, cache_dir):
        input = f'{cache_dir}/text/{self.checksum}.txt'
        output = f'{cache_dir}/dates/{self.checksum}.txt'

        if not pathlib.Path(input).exists():
            return

        if pathlib.Path(output).exists():
            with open(output, 'r') as src:
                self.date = src.read().strip()
            return

        with open(input, 'r') as src:
            content = src.read()
            words = content.split()
            first_10_procent = words[:int(len(words) * 0.1)]

            date = ''

            for word in first_10_procent:
                if dates.is_date(word):
                    date = word
                    break

            with open(output, 'w') as out:
                out.write(date)

        self.date = date

    def parse_title(self, cache_dir):
        input = f'{cache_dir}/pdfs/{self.checksum}.pdf'
        output = f'{cache_dir}/titles/{self.checksum}.txt'

        if not pathlib.Path(input).exists():
            return

        if pathlib.Path(output).exists():
            with open(output, 'r') as src:
                self.title = src.read().strip()
            return

        with open(input, 'rb') as src:
            try:
                docinfo = PdfFileReader(src).getDocumentInfo()
                if '/Title' not in docinfo:
                    return

                title = docinfo['/Title']
                with open(output, 'w') as out:
                    out.write(title)
            except Exception as e:
                print(e)
                return


        self.title = title
