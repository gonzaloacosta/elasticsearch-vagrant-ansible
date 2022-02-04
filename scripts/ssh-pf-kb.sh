#!/bin/bash

world="0.0.0.0"
desktop="192.168.0.10"
kb_ip="192.168.28.77"
kb_port="5601"
kb_user="vagrant"
ssh_key=".vagrant/machines/kb/virtualbox/private_key"


case $1 in

  pf)
    echo "Expose Kibana ($kb_ip:$kb_port) in Desktop ($desktop) to World ($world:$kb_port)"
    ssh -L $kb_port:$world:$kb_port -i $ssh_key $kb_user@$kb_ip &
    ;;

  laptop)
    echo "Test Kibana from laptop to desktop"
    curl -s http://$desktop:$kb_port
    ;;

  *)
    echo "No option avalable"

esac


