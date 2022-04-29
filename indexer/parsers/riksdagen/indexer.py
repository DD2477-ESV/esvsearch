from .. import constants
import os
import re
import codecs
import time
from bs4 import BeautifulSoup
from . import index_definitions
from dateutil.parser import parse
from elasticsearch import Elasticsearch


es = Elasticsearch(constants.ELASTICSEARCH_ENDPOINT)
TYPE_TO_INDEX = {'dir': "kommittédirektiv", 'komm': 'kommittéberättelser', 'prop': 'propositioner', 'ds': 'departementsserien', "sou": 'sou'}


def extract_text_from_html(html):
    """Cleans up html by removing styles + scripts and removing surplus blank space
    Arguments:
    html : the html to be cleaned up
    Returns :
    dict : {"text" : Cleaned up text (string)}
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Remove styles and scripts
    [elem.extract() for elem in soup(['style', 'script'])]
    text = soup.getText()

    # Replace multiple spaces with a single space
    text = re.sub('[^\\S\\n]+', ' ', text)
    # Replace multiple newlines with a single newline
    text = re.sub('\\n+', '\\n', text)
    return {
        "text": text
    }


def index_all_files(input_files_root):
    """Walks the directory tree starting at input_files_root,
    extracting html and relevant metadata from each xml-file encountered
    and indexes it into a Elasticsearch index.
    Provides a rough estimate of the time to finish indexing after each document.
    Arguments:
    input_files_root : the base directory containing the xml files
    """
    count = 1
    count_size = 0
    tot_count = 0
    tot_size = 0
    ETA = 0.0

    for root, dirs, files in os.walk(input_files_root):
        for file in files:
            if file.endswith(".xml"):
                rel_dir = os.path.relpath(root, input_files_root)
                relative_path_to_file = os.path.join(rel_dir, file)
                abs_file_path = os.path.join(input_files_root, relative_path_to_file)
                tot_size += os.path.getsize(abs_file_path)
                tot_count += 1
        start = time.perf_counter()
        for file in files:
            if file.endswith(".xml"):
                rel_dir = os.path.relpath(root, input_files_root)
                relative_path_to_file = os.path.join(rel_dir, file)
                abs_file_path = os.path.join(input_files_root, relative_path_to_file)
                if count > 1:
                    ETA = (time.perf_counter() - start) / count_size * (tot_size - count_size ) / 60
                    print("indexing from %s , document number : %d / %d , ETA : %.2f min" % (relative_path_to_file, count, tot_count, ETA))
                count_size += os.path.getsize(abs_file_path)
                count += 1
                with codecs.open(abs_file_path, encoding='utf-8') as infile:
                    content = infile.read()
                    soup = BeautifulSoup(content, "xml")
                    try:
                        html = soup.find_all('html')[0].string

                        json_to_index = extract_text_from_html(html)
                        id = soup.find_all('dok_id')[0].string
                        json_to_index['id'] = id

                        title = soup.find_all('titel')[0].string
                        json_to_index['title'] = title

                        doc_url = soup.find_all("dokument_url_html")[0].string
                        json_to_index["url"] = doc_url

                        organ = soup.find_all('organ')[0].string
                        json_to_index['organ'] = organ

                        # As we are using type for the index, we'll leave subtype as the documents type
                        # (trying to be consistent with what's available from other agencies)
                        subtyp = soup.find_all('subtyp')[0].string
                        json_to_index['type'] = subtyp

                        date = soup.find_all('publicerad')[0].string[:10]
                        json_to_index['date'] = parse(date)

                        typ = soup.find_all('typ')[0].string

                        # use the 'typ' property in conjunction with the parser as index
                        if typ in TYPE_TO_INDEX:
                            index_name = f'riksdagen_{TYPE_TO_INDEX[typ]}'
                        else:
                            index_name = f'riksdagen_övrigt'
                        index_exists = es.indices.exists(index=index_name)
                        if not index_exists:
                            print(f'creating the index {index_name}')
                            request_body = {
                                'settings': index_definitions.INDEX_SETTINGS,
                                'mappings': index_definitions.INDEX_MAPPINGS
                            }
                            es.indices.create(index=index_name, body=request_body)

                        es.index(
                            index=index_name,
                            id=id,
                            body=json_to_index
                        )
                    except IndexError:
                        print('No HTML available in document : %s' % (relative_path_to_file))
                        continue
