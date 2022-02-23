# ElasticSearch

The main repo contain all necesary to play with elasticsearch. To spin up the environment follow the next commands.

## Pre requisites

- VirtualBox already installed in your host.
- Vagrant
- Internet connection

## Spin up environment

1. Create Boxes.

```bash
vagrant up
```

2. Deploy Elasticsearch software

```bash
ansible-playbook playbook.yml
```

3. Check if elasticsearch is up and running

```bash
curl http://192.168.28.71:9200
curl http://192.168.28.71:9200/_cat/nodes
curl http://192.168.28.71:9200/_cat/health
```

Take time to deploy all the environment.

## Enable TLS

- [Setting up TLS on a cluster](https://www.elastic.co/guide/en/elasticsearch/reference/7.5/ssl-tls.html)
- [Encrypting communication](https://www.elastic.co/guide/en/elasticsearch/reference/7.5/configuring-tls.html#tls-transport)


