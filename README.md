# ESV Search

## Usage

### Start the frontend

```bash
cd frontend-react/
npm ci
npm run start

# should now be available at http://localhost:3000
```


### Launch a docker instance

To start an elasticsearch instance on localhost:9200 using docker

```bash
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "http.cors.enabled=true" -e "http.cors.allow-origin=/http?:\/\/localhost(:[0-9]+)?/" docker.elastic.co/elasticsearch/elasticsearch:8.1.2
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

### Index Riksdagen

Download the relevant zip files from [riksdagens website](https://data.riksdagen.se/data/dokument)

```bash
wget https://data.riksdagen.se/dataset/dokument/prop-2018-2021.xml.zip -O /tmp/prop-2018-2021.xml.zip
unzip /tmp/prop-2018-2021.xml.zip -d /tmp/prop-2018-2021
```

Run the indexer

```bash
python indexer/main.py riksdagen /tmp/prop-2018-2021
```

Index is now available at

```bash
$ curl "http://localhost:9200/riksdagen_propositioner/_stats"
```
Riksdagen documents are automatically indexed into one of the following indices depending on document type:
- Kommittédirektiv
:  http://localhost:9200/riksdagen_kommittédirektiv
- Kommittéberättelser
:  http://localhost:9200/riksdagen_kommittéberättelser
- Propositioner
:  http://localhost:9200/riksdagen_propositioner
- Departementsserien
:  http://localhost:9200/riksdagen_departementsserien
- Statliga offentliga utredningar
:  http://localhost:9200/riksdagen_sou
- Övrigt
:  http://localhost:9200/riksdagen_övrigt

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
