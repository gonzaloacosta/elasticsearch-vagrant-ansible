from elasticsearch import Elasticsearch
import logging
import json


index = "salads"
hosts = [
            '192.168.28.71:9200', 
            '192.168.28.72:9200', 
            '192.168.28.73:9200', 
        ]

def es_connect(): 
    es = None
    es = Elasticsearch(
            hosts,
            use_ssl=True,
            verify_certs=False,
            ca_certs=None,
            ssl_show_warn=False
            )
    if es.ping():
        print("Connected to Elasticsearch!")
    else:
        print("Not Connected to Elasticsearch!")
    return es

def create_index(es_object, index):
    created = False
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "salads": { 
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "submitter": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "calories": {
                        "type": "integer"
                    },
                    "ingredients": {
                        "type": "nested",
                        "properties": {
                            "step": {"type": "text"}
                        }
                    }
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index=index):
            es_object.indices.create(
                                    index=index,
                                    ignore=400,
                                    body=load_json(settings)
                                )
        print('Created Index {}'.format(index))
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created
        
def store_record(es_object, index, data):
    is_stored = True
    try:
        outcome = es_object.index(
                    index=index,
                    doc_type='_doc',
                    document=json.dumps(data)
                )
        #print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored

def store_records(es_object, index, data):
    result = []
    if not data:
        print("Data is empty")
        is_all_stored = False
    for doc in data:
        is_stored = store_record(es_object, index, doc)
        if not is_stored:
            print("Record not stored: {}".format(doc["tittle"]))
        else:
            print("Record stored: {}".format(doc["tittle"]))
        result.append({ doc["tittle"], is_stored })
    return result

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    data = [
        {
            "tittle": "Rice Salad",
            "submitter": "gonzalo.acosta@quark.com",
            "description": "Rice salad with oil, pepper and salt",
            "calories": 100 
        },
        {
            "tittle": "Pasta Salad",
            "submitter": "gonzalo.acosta@quark.com",
            "description": "Pasta salad with oil, pepper and salt",
            "calories": 100 
        },
        {
            "tittle": "Fruit Salad",
            "submitter": "gonzalo.acosta@quark.com",
            "description": "Fruit salad", 
            "calories": 50 
        }
    ]

    es = es_connect()
    create_index(es, index)
    store_records(es, index, data)
