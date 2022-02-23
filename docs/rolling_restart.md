# Rolling restart

Start with GREEN cluster state

```
GET _cat/health
GET _cat/nodes
```

Stop primary shards re allocation

```
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "primaries"
  }
}
```

Flush operation indexing

```
POST _flush/synced
```

Restart services in one node

```
# sudo systemctl restart elasticsearch
# sudo systemctl status elasticsearch
```

At this moment cluster will be stay in YELLOW, and re enable allocation

```
GET _cat/nodes

PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": null
  }
}
```

Waiting to cluster in GREEN and repeate with another nodes
