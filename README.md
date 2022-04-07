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
