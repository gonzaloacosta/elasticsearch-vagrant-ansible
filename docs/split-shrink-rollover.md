# Split, shrink and rollover operation

1. User ingest script to upload sample documents.

For example data execute `python3 scripts/import-data.py`

```
GET _cat/indices/kibana_sample_data_*
GET _cat/indices/quark-countries-*
```

2. Run a search and check the numbers of shards (1) and documents (576250)

```
GET quark-countries-2022-01-30/_search?size=0
```

3. Split into 10 shards

```
POST quark-countries-2022-01-30/_split/quark-coutries-2022-01-30-target
{
  "settings": {
    "index.number_of_shards": 10
  }
}
```

NOTE: when execute this tasks output show us that the index need to be in Read Only.

```
{
  "error" : {
    "root_cause" : [
      {
        "type" : "illegal_state_exception",
        "reason" : "index quark-countries-2022-01-30 must be read-only to resize index. use \"index.blocks.write=true\""
      }
    ],
    "type" : "illegal_state_exception",
    "reason" : "index quark-countries-2022-01-30 must be read-only to resize index. use \"index.blocks.write=true\""
  },
  "status" : 500
}
```

4. Edit the index setting and add "index.blocks.write: true"

```
PUT quark-countries-2022-01-30/_settings
{
  "settings": {
    "index.blocks.write": true
  }
}
```

```
GET quark-countries-2022-01-30/_settings

```

```
{
  "quark-countries-2022-01-30" : {
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "blocks" : {
          "write" : "true"
        },
        "provided_name" : "quark-countries-2022-01-30",
        "creation_date" : "1645649885116",
        "number_of_replicas" : "1",
        "uuid" : "CBqMr7SQQZGWvqGaySYMew",
        "version" : {
          "created" : "7110199"
        }
      }
    }
  }
}
```

5. Split into 10 shards

```
POST quark-countries-2022-01-30/_split/quark-countries-2022-01-30-target
{
  "settings": {
    "index.number_of_shards": 10
  }
}
```

```
GET quark-countries-2022-01-30/_settings
GET _cat/indices/quark*
GET _cat/shards/quark-countries-2022-01-30-target
```

Waiting some time to re distribute and re allocating all new  10 shareds across all nodes. in this case operation will be take 10 min prox with 1 index with 1 primary and 1 replica.

## Shirnk operation

```
GET /_cat/shards/quark-countries-2022-01-30-target*?v&h=index,shard,prirep,state,docs,node

GET /_cat/indices/quark-countries-2022-01-30-target
```

1. We need to put in read only the index and all the shards in the same node.

```
PUT quark-countries-2022-01-30-target/_settings
{
  "settings": {
    "index.number_of_replicas": 0,
    "index.routing.allocation.require._name": "esd2",
    "index.blocks.write": true
  }
}
```

```
GET /_cat/shards/quark-countries-2022-01-30*?v&h=index,shard,prirep,state,docs,node
GET quark-countries-2022-01-30-target/_settings
```

2. Shrink operation

```
POST /quark-countries-2022-01-30-target/_shrink/quark-countries-2022-01-30-shrunk
{
  "settings": {
    "index.routing.allocation.require._name": null,
    "index.blocks.write": null,
    "index.number_of_replicas": 1,
    "index.number_of_shards": 10
  }
}
```

```
PUT quark-countries-2022-01-30-shrunk/_settings
{
  "settings": {
    "index.number_of_replicas": 1
  }
}
```

```
GET /_cat/shards/quark-countries-2022-01-30*?v&h=index,shard,prirep,state,docs,node

GET quark-countries-2022-01-30/_search?size=0

GET quark-countries-2022-01-30-shrunk/_search?size=0
```


## Rollover

Create a new indexs in base a certain conditions

Create an index template for the `quark-cities-*` indices.

```
PUT _index_template/quark-cities-rollover
{
  "template": {
    "mappings": {
      "properties": {
        "foo": {
          "type": "keyword"
        }
      }
    },
    "aliases": {
      "quark-cities": {}
    }
  },
  "index_patterns": [
    "quark-cities-*"
  ]
}
```

```
GET _cat/templates
```

2. Create an index rollover with demo rollover write

```
PUT quark-cities-000001
{
  "aliases": {
    "quark-cities-write": {}
  }
}
```

3. Put some documents with scripts/run.sh

```
POST quark-cities-write/_doc
{
  "foo": "bar"
}
```

4. Check the number of documents

```
GET quark-cities-write/_search
{
  "size": 0,
  "aggs": {
    "index": {
      "terms": {
        "field": "_index",
        "order": {
            "_key": "asc"
        }
      }
    }
  }
}
```

5. Run rollover

```
POST /quark-cities-write/_rollover
{
  "conditions": {
    "max_age": "7d",
    "max_docs": 100,
    "max_size": "5mb"
  }
}
```

6. Check indices

```
GET quark-cities-write/_search?size=0

GET _cat/indices/quark-cities*
```
