for i in $(seq 1 1200) ; do curl -ks -XPOST "https://192.168.28.71:9200/quark-cities-write/_doc" -H 'Content-Type: application/json' -d'{  "foo": "bar"}' ; echo "" ; done

