from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
from elasticsearch_dsl import Search
import time
import pandas as pd

import json

#countries_index = "quark-countries-2022-01-25"
countries_index = "quark-countries-2022-01-30"
dataset_path = "../datasets/countries.json"
es_hosts=['http://192.168.28.71:9200', 'http://192.168.28.72:9200', 'http://192.168.28.73:9200']
search_capital="Buenos Aires"
start_time = time.time()
seconds = 3000
count = 0

print("Open dataset path: {}".format(dataset_path))

with open(dataset_path) as f:
    data = json.load(f)

df = pd.DataFrame(data, columns = [ 
    "id",
    "name",
    "iso3",
    "iso2",
    "numeric_code",
    "phone_code",
    "capital",
    "currency",
    "currency_name",
    "currency_symbol",
    "tld",
    "native",
    "region",
    "subregion",
    "timezones",
    "translations",
    "latitude",
    "longitude",
    "emoji",
    "emojiU"
])

print("Open Elasticsearch connection to host: {}".format(es_hosts))

es_client = connections.create_connection(hosts=es_hosts)

def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
            "_index": countries_index,
            "_source": document,
        }

while True:

    print("Bulk document to Elasticsearch iteration number: {} ".format(str(count)))

    try:
        helpers.bulk(es_client, doc_generator(df))
        current_time = time.time()
        elapsed_time = current_time - start_time
        count = count + 1 

    except Exception as ex: 

        print("Exception: {} and Iteration: {}".format(str(ex),str(int(elapsed_time))))
        continue

    else:

        if elapsed_time > seconds:
            print("Finished iterating in: "+ str(int(elapsed_time)))
            break

print("Perform small search for capital {}".format(search_capital))

s = Search(index=countries_index).query("match", capital=search_capital)

response = s.execute()

for hit in response:
    print(hit.meta.score, hit.name)
