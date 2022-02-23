# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "centos/7"
  config.ssh.insert_key = true
  config.vm.synced_folder ".","/vagrant", disabled: true

  config.vm.provider:virtualbox do |v|
    v.memory = 2048
    v.cpus = 2
    v.linked_clone = true
  end

  config.vm.define "esd1" do |elk|
    elk.vm.hostname = "esd1.test"
    elk.vm.network:private_network, ip:"192.168.28.71"
    elk.vm.provider :virtualbox do |v|
      v.memory = 4096
      v.cpus = 2
    end
  end

  config.vm.define "esd2" do |elk|
    elk.vm.hostname = "esd.test"
    elk.vm.network:private_network, ip:"192.168.28.72"
    elk.vm.provider :virtualbox do |v|
      v.memory = 4096
      v.cpus = 2
    end 
  end

  config.vm.define "esd3" do |elk|
    elk.vm.hostname = "esd3.test"
    elk.vm.network:private_network, ip:"192.168.28.73"
    elk.vm.provider :virtualbox do |v|
      v.memory = 4096
      v.cpus = 2
    end
  end

  config.vm.define "esd4" do |elk|
    elk.vm.hostname = "esd4.test"
    elk.vm.network:private_network, ip:"192.168.28.78"
    elk.vm.disk :disk, name: "data", size: "2GB"
    elk.vm.provider :virtualbox do |v|
      v.memory = 2048
      v.cpus = 2
    end
  end

  config.vm.define "esd5" do |elk|
    elk.vm.hostname = "esd5.test"
    elk.vm.network:private_network, ip:"192.168.28.79"
    elk.vm.provider :virtualbox do |v|
      v.memory = 2048
      v.cpus = 2
    end
  end

  config.vm.define "esm1" do |elk|
    elk.vm.hostname = "esm1.test"
    elk.vm.network:private_network, ip:"192.168.28.74"
  end

  config.vm.define "esm2" do |elk|
    elk.vm.hostname = "esm2.test"
    elk.vm.network:private_network, ip:"192.168.28.75"
  end

  config.vm.define "esm3" do |elk|
    elk.vm.hostname = "esm3.test"
    elk.vm.network:private_network, ip:"192.168.28.76"
  end

  config.vm.define "kb" do |elk|
    elk.vm.hostname = "kb.test"
    elk.vm.network:private_network, ip:"192.168.28.77"
    elk.vm.network:forwarded_port, guest:5601, host: 5601
  end

end
