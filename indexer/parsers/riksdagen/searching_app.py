"""
Code modified from : https://github.com/alexander-marquardt/es_local_indexer
"""

from flask import Flask, request, render_template, send_from_directory
from elasticsearch import Elasticsearch

INDEX_NAME = "riksdagen"
DOC_PATH = "G:\\Riksdagsdata\\Statliga_utredningar"

es = Elasticsearch("http://localhost:9200")
app = Flask(__name__)

@app.route('/')
def my_form():
    """Generates the html for the home page
    """
    return render_template('home_page.html',
                                     search_text='',
                                     input_files_root=app.config['input_files_root'],
                                     index_name=app.config['index_name'])


@app.route('/', methods=['POST'])
def my_form_post():
    """Generates the html for the home page if a post is received. In other words, this
    generates the html in response to a search request.
    """
    search_text = request.form['search_text'].lower()

    try:
        last_score = request.form['last_score']
        last_id = request.form['last_id']
        optional_search_after = '"search_after": [%s, "%s"],' % (last_score, last_id)
    except:
        optional_search_after = ''


    
    body = render_template("search_body.json",
                           query_string=search_text,
                           optional_search_after=optional_search_after) # Skapa en query från .json-fil

    search_result = es.search(index=app.config['index_name'], body=body)  # Söka med denna query i angivet index
    all_hits = search_result["hits"]["hits"] # Få fram alla funna dokument
    
    generated_html = render_template('show_search_results.html',
                                    search_text=search_text,
                                    input_files_root=app.config['input_files_root'],
                                    index_name=app.config['index_name'],
                                    pages=all_hits)

    return generated_html


@app.route('/elastic_offline_search/original/<path:relative_path>')
def open_file_on_filesystem(relative_path):
    """Generates the html that shows the original HTML file. (this is necessary because
    browser security won't allow linking directly to html files on the filesystem)
    """
    return send_from_directory(app.config['input_files_root'], relative_path)


@app.route('/elastic_offline_search/cached/<_id>')
def show_cached_file_contents(_id):
    """Generates the html that shows content field in the document indicated by the _id value
    """
    es_doc = es.get(index=app.config['index_name'], id=_id)
    return render_template("cached_text.html",
                           cached_text = es_doc['_source']['content'])



def configure_global_app():
    """Sets fields in app.config based on the command line parameters. These values are used in various
    parts of the search code.
    """
    # parsed_args = common.parse_arguments()
    app.config['input_files_root'] = DOC_PATH
    app.config['index_name'] = INDEX_NAME
    print('Files root: %s. Index name: %s', app.config['input_files_root'], app.config['index_name'])
    return


if __name__ == '__main__':
    """Start the search application
    """
    configure_global_app()
    app.run()