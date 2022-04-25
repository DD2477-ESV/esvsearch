# ESV Search

## Project Outline

- Indexerings Job
  1. Sätta upp elastic (på port :9200)
  2. `$ python index.py path_to_xml_directory`
     - parsa alla dokument
     - plocka ur text och taggar
     - skicka in alla doc i ES
  3. `$ python manage_index.py`
     (- enkelt kunna rensa index)
  4. andra datakällor
  5. webcrawl för att ladda ner xml:erna

- Sök interface
  1. skapa en django app
  2. en sida med sök ruta
  3. submit av sök input skickar query till elasticsearch
  4. matchande dokumenten renderas i söksidan
  5. klicka på sökresultat visar dokumentet
  6. mer avancerade sökfilter
     - kategorier
     - datum
     - etc.

## Usage


### Launch a docker instance

To start an elasticsearch instance on localhost:9200 using docker

```bash
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.2
```

### Index Arbetsförmedlingen

#### Setup a python environment

```bash
# Tested with python 3.10.3
$ python --version
Python 3.10.3

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Run the indexer

```bash
$ python indexer/main.py arbetsformedlingen /tmp/arbetsformedlingen
```

Output should be something like the following

```console
fetching docs
crawling src............................................done.
found 433 docs
Fetching titles... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Fetching PDFs... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Parsing Text... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Parsing Dates... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

Around 400 docs should now have been indexed

```bash
$ curl "http://localhost:9200/arbetsformedlingen/_stats"
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_all": {
    "primaries": {
      "docs": {
        "count": 433,
        "deleted": 0
      },
   ...
```

#### Example queries

Get the reports from the last year

```bash
$ curl -X "POST" "http://localhost:9200/arbetsformedlingen/_search" \
     -H 'Content-Type: application/json' \
     -d $'{
  "fields": [
    "url",
    "download_url",
    "date",
    "title"
  ],
  "query": {
    "range": {
      "date": {
        "gte": "now-1y",
        "lt": "now/d"
      }
    }
  },
  "_source": false,
  "sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ]
}'
```

Match query for `"arbetsmarknadsprognos stockholm"`

```bash
$ curl -X "POST" "http://localhost:9200/arbetsformedlingen/_search" \
     -H 'Content-Type: application/json' \
     -d $'{
  "fields": [
    "url",
    "download_url",
    "date",
    "title"
  ],
  "query": {
    "match": {
      "title": {
        "query": "Arbetsmarknadsprognos stockholm",
        "operator": "and"
      }
    }
  },
  "_source": false,
  "sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ]
}'
```

### Index BRÅ

Follows a similar install procedure to arbetsförmedlingen. To index, run the following command

```bash
$ python indexer/main.py bra /tmp/bra
```

Index available here

```bash
$ curl "http://localhost:9200/bra/_stats"
```

### Index MSB

```bash
$ python indexer/main.py msb /tmp/msb
```

Index available here

```bash
$ curl "http://localhost:9200/msb/_stats"
```

### Index FHM

```bash
$ python indexer/main.py fhm /tmp/fhm
```

Index available here

```bash
$ curl "http://localhost:9200/fhm/_stats"
```

### Index Försäkringskassan

```bash
$ python indexer/main.py forsakringskassan /tmp/forsakringskassan
```

Index available here

```bash
$ curl "http://localhost:9200/forsakringskassan/_stats"
```

### Index ESV

```bash
$ python indexer/main.py esv /tmp/esv
```

Index available here

```bash
$ curl "http://localhost:9200/esv/_stats"
```

### Index Polisen

```bash
$ python indexer/main.py polisen /tmp/polisen
```

Index available here

```bash
$ curl "http://localhost:9200/polisen/_stats"
```

### Index PTS

```bash
$ python indexer/main.py pts /tmp/pts
```

Index available here

```bash
$ curl "http://localhost:9200/pts/_stats"
```

### Index FI

```bash
$ python indexer/main.py fi /tmp/fi
```

Index available here

```bash
$ curl "http://localhost:9200/fi/_stats"
```

### Index Riksbanken

```bash
$ python indexer/main.py riksbanken /tmp/riksbanken
```

Index available here

```bash
$ curl "http://localhost:9200/riksbanken/_stats"
```

### Index FOI

```bash
$ python indexer/main.py foi /tmp/foi
```

Index available here

```bash
$ curl "http://localhost:9200/foi/_stats"
```

### Index Socialstyrelsen

```bash
$ python indexer/main.py socialstyrelsen /tmp/socialstyrelsen
```

Index available here

```bash
$ curl "http://localhost:9200/socialstyrelsen/_stats"
```
