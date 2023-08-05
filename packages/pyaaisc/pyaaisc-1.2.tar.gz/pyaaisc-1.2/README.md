# pyaaisc
Python AAindex database scrape

### About

`pyaaisc` scrapes data from AAindex website https://www.genome.jp/aaindex/. 

Currently supported operations:
* search by `keyword` and `dbkey`
* get full list of indices by `dbkey`
* get a single record by `accession_number` and `dbkey`

### Instalation

```
pip install pyaaisc
```

### Usage

```python
from pyaaisc import Aaindex

aaindex = Aaindex()
for result in aaindex.search('charge'):
    print(result)

full_list = aaindex.get_all(dbkey='aaindex1')

record = aaindex.get('KLEP840101')
title = record.title
index_data = record.index_data

```