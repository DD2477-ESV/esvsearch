from .. import constants
import os
import re
import codecs
import time
from bs4 import BeautifulSoup
from . import index_definitions
from elasticsearch import Elasticsearch


es = Elasticsearch(constants.ELASTICSEARCH_ENDPOINT)

def extract_text_from_html(html_body):
    """Receives html and removes styles and scripts.
    Keyword arguments:
    html_body -- the html that we will be cleaning up
    """
    soup = BeautifulSoup(html_body, 'html.parser')

    # Remove styles and scripts from the html for ingestion into the contents
    [s.extract() for s in soup(['style', 'script'])]
    visible_text = soup.getText()

    # Replace multiple spaces with a single space
    visible_text = re.sub('[^\\S\\n]+', ' ', visible_text)
    # Replace multiple sequential newlines with a single newline
    visible_text = re.sub('\\n+', '\\n', visible_text)
    return {
        "content": visible_text
    }


def walk_and_index_all_files(input_files_root, index_name):
    """Walks the directory tree starting at base_dir, and ingests each xml document that
    is encountered into an Elasticsearch index
    Keyword arguments:
    input_files_root -- the base directory which the html files reside in
    index_name -- name of the index that will be used
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
                    print("indexing %s from %s , document number : %d / %d , ETA : %.2f min" % (index_name, relative_path_to_file, count, tot_count, ETA))
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
                        json_to_index['titel'] = title
                        
                        doc_url = soup.find_all("dokument_url_html")[0].string
                        
                        json_to_index["dok_url"] = doc_url
                        organ = soup.find_all('organ')[0].string
                        json_to_index['organ'] = organ

                        subtyp = soup.find_all('subtyp')[0].string
                        json_to_index['subtyp'] = subtyp

                        typ = soup.find_all('typ')[0].string
                        json_to_index['typ'] = typ
                        
                        date = soup.find_all('publicerad')[0].string[:10]
                        json_to_index['date'] = date
                        
                        es.index(
                            index=index_name,
                            id=id,
                            body=json_to_index
                        )
                    except IndexError:
                        print('No HTML available in document : %s' % (relative_path_to_file))
                        continue


def configure_index(index_name):
    """Ensures that settings and mappings are defined on the Elasticsearch
     index that we will write our documents into.
    Keyword arguments:
    index_name -- name of the index that will be used
    """
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        print("Index: %s already exists. Would you like to delete, append, or abort" % index_name)
        answer = input('Type one of [O]verwrite, [A]ppend or [C]ancel: ')
        # answer = 'append'
        if answer.lower() == 'o':
            es.indices.delete(index=index_name, ignore=[400, 404])
            index_exists = False
        elif answer.lower() == 'c':
            exit(0)

    # If the index doesn't exist, then write settings/mappings
    if not index_exists:
        request_body = {
            'settings': index_definitions.INDEX_SETTINGS,
            'mappings': index_definitions.INDEX_MAPPINGS
        }
        es.indices.create(index=index_name, body=request_body)
