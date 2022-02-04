from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
import pandas as pd


# initialize list of lists
data = [['tom', 10, 'NY'], ['nick', 15, 'NY'], ['juli', 14, 'NY'], ['akshay', 30, 'IND'], ['Amit', 14, 'IND']]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns = ['Name', 'Age', 'Country'])

from elasticsearch import Elasticsearch
from elasticsearch import helpers

es_client = connections.create_connection(hosts=['http://192.168.28.71:9200/'])
def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
                "_index": 'quark-customer-age',
                "_source": document,
            }

helpers.bulk(es_client, doc_generator(df))

#get data from elastic search
from elasticsearch_dsl import Search
s = Search(index="age_sample").query("match", Name='nick')
