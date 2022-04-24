from .. import constants
import os
import re
import codecs
from xml.dom import minidom
from bs4 import BeautifulSoup
from bs4.element import Comment
from . import index_definitions
from elasticsearch import Elasticsearch


es = Elasticsearch(constants.ELASTICSEARCH_ENDPOINT)


def extract_fields_from_html(html_body):
    """Receives html and removes styles and scripts.

    (could be easily modified to remove more if necessary).
    Keyword arguments:
    html_body -- the html that we will be cleaning up
    """
    soup = BeautifulSoup(html_body, 'html.parser')

    # Get the title from the html. However, some pages just redirect to others,
    # and so might not have a title set
    try:
        title = soup.title.contents[0]
        title = re.sub('\\s+', ' ', title)
    except:
        title = ""

    # Remove styles and scripts from the html for ingestion into the contents
    [s.extract() for s in soup(['style', 'script'])]
    visible_text = soup.getText()

    # The following lines cleanup the text for better display when "View indexed content"
    # is selected. This leaves in a single newline when multiple \\n are encountered.
    #
    # Replace multiple spaces with a single space, but leave newlines in for now
    visible_text = re.sub('[^\\S\\n]+', ' ', visible_text)
    # Replace multiple sequential newlines with a single newline
    visible_text = re.sub('\\n+', '\\n', visible_text)
    return {
        "title": title,
        "content": visible_text
    }


def walk_and_index_all_files(input_files_root, index_name):
    """Walks the directory tree starting at base_dir, and ingests each html document that
    is encountered into an Elasticsearch index
    Keyword arguments:
    index_name -- name of the index that will be used
    input_files_root -- the base directory which the html files reside in
    """

    for root, dirs, files in os.walk(input_files_root):
        for file in files:
            if file.endswith(".xml"):
                rel_dir = os.path.relpath(root, input_files_root)
                relative_path_to_file = os.path.join(rel_dir, file)
                print("indexing %s from %s" % (index_name, relative_path_to_file))

                abs_file_path = os.path.join(input_files_root, relative_path_to_file)
                with open(abs_file_path) as infile:
                    content = infile.read()
                    soup = BeautifulSoup(content, "xml")
                    html = soup.find_all('html')[0].string

                    json_to_index = extract_fields_from_html(html)

                    id = soup.find_all('dok_id')[0].string
                    json_to_index['id'] = id

                    organ = soup.find_all('organ')[0].string
                    json_to_index['organ'] = organ

                    subtyp = soup.find_all('subtyp')[0].string
                    json_to_index['subtyp'] = subtyp

                    typ = soup.find_all('typ')[0].string
                    json_to_index['typ'] = typ

                    es.index(
                        index=index_name,
                        id=id,
                        body=json_to_index
                    )


def configure_index(index_name):
    """Ensures that settings and mappings are defined on the Elasticsearch
     index that we will write our documents into.
    Keyword arguments:
    index_name -- name of the index that will be used
    """
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        # print("Index: %s already exists. Would you like to delete, append, or abort" % index_name)
        # answer = input("Type one of 'overwrite', 'append' or 'abort': ")
        answer = 'overwrite'
        if answer == "overwrite":
            es.indices.delete(index=index_name, ignore=[400, 404])
            index_exists = False
        elif answer == "abort":
            exit(0)

    # If the index doesn't exist, then write settings/mappings
    if not index_exists:
        request_body = {
            'settings': index_definitions.INDEX_SETTINGS,
            'mappings': index_definitions.INDEX_MAPPINGS
        }
        es.indices.create(index=index_name, body=request_body)
