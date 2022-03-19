# Red Elasticsearch Cluster Panic No Longer

The cluster allocation explain API (explain API) was designed to answer two fundamental questions:

1. For unassigned sahrds: "Why are my shards unassigned?"
2. For assigned shards: "Why are my shards assigned to this particualr node?"

## What is shards allocation?

Shard allocation is the process of assigning a shard to a node in the cluster. In order to scale to hug document set and provide high availability in the face of node failure, Elasticsearch splits an index's document into shards, each shard residing on a node in a cluter. If a primary shards cannot be allocated, the index will be missing data and/or no new document can be written into the index. If replica shards cannot be allocated, the cluster risk of losing data in case of permanent failure (e.g corrupt disks) of the node holding the primary shard. If shard is allocated but to slower-than-desider node, them the shards of high traffinc indices will suffer from being located but to slower machine and the performance of the cluster will degrade. Therefore, allocating shads and assigning them to the best node possible is tof fundamentl importance within Elasticsearch.

The shard allocation process differs for newly created indices and existing indices. In bot case, Elasticsearch has to main compnent at work: *allocators and deciders*. Allocators try to find the best (defined below) nodes to hold the shards, and deciders make the decision if allocating to a node is allowed.

For newly crated indices, the allocator look for the nodes with those having the lest shard weight appearing first. Thus, the allocator's gol for a newly create indes is to assigne the index' shards to nodes in manner tat would result in the most balanced cluster. The decider then take each node in order and decide ifthe shard is allowe to be allocated to that node. For example, if filter allocation rule set up to prevent node A from holding any shard of index idx, then the filter decider will prevent allocation of idxs' shard to node A, even though it may be ranked first by allocator as the best node from cluster balancing perspective. not that the allocator only take ninto account the number of shard per node, not the size of easch shard. It is the job of one of the deciders to prevent allocation to nodes that exced a certain dis occupancy thrshold.

For existing indices, we must further distinguish between primary and replica shads. For primary shard, the allocator will *only* allow allocation to an node that alreday holds a known good copy of the shard. If the allocator didn't take such a step, the allocatin a primary sahds to a node that dest not already have an up-to-date copy of the shard will result in data loss!. In the cse of replica shard, teh allocator first look to see if there are already copies of the sahrds (even stale copies) on the nodes. If so, teh allocator will prioritize assigning the shards to one of the nodes holding copy, because the replica need to get in-sync with the primary once it is allocated, and fact that a node already has some of the sahrd data means (hopefully) a lot oess data has to be copied over to the replica from the primary. This can speed up the recovery process for the replica shards significanlty.

## Diagnosing Unassigned Primary Shards.

Having an unassigned shard is one of the worst thing that can happen in a cluster. if the unassigned primary is on a newly created index, no document can be written to that index. If the unassigned primary is on an existing index, then not only can the index not be written to, but all data previusly indexed is unavailable for searching!.

Let's start with some test to explain whats happend in each situation.

```
PUT /test_idx?wait_for_active_shards=0
{
  "settings":
  {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.routing.allocation.exclude._name": "esd1,esd2,esd3"
  }
}
```

Due a filter allocation rules, the index will be created but none of this nodes can be receive the shards and the index will be put in *RED* with unassigned primary shards. We can try found explanation in explain API

```
GET /_cluster/allocation/explain
```

The explain is very useful, the shars cannot be allocated in any nodes because not pass the filter exclude.


```
PUT /test_idx/_settings
{
  "index.routing.allocation.exclude._name": null 
}
```

And test again the result

```
GET /_cluster/allocation/explain 
{ 
   "index": "test_idx", 
   "shard": 0, 
   "primary": true
}
```

Shard will be allocated in a new available nodes.

## Diagnosing Unassigned Replica Shards

Let's put our existing *test_idx* and increase the number of replicas.

```
PUT /test_idx/_settings
{
  "number_of_replicas": 1
}
```

Now check in with nodes has been schedul new replicas shards

```
GET /_cat/shards/test_idx
```

Then reboot or stop the node that has replica shards and query to explain API again. We learn from this output that the replica shards cannot be allocated because for node B, the filter allocation rules prevented allocation to it. Since node A already holds the primary shard, another copy of the shard cannot be assigned to it.

