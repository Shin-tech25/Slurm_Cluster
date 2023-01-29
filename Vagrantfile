Vagrant.require_version ">= 1.7.0"

Vagrant.configure("2") do |config|
  if Vagrant.has_plugin?("vagrant-vbguest")
    config.vbguest.auto_update = false  
  end

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 2
    vb.memory = 2048
  end

  config.ssh.insert_key = false
  config.ssh.private_key_path = '~/.vagrant.d/insecure_private_key'

  config.vm.define "mnode" do |mnode|
    mnode.vm.box = "generic/rocky8"
    mnode.vm.box_version = "4.2.8"
    mnode.vm.hostname = "mnode.prometech.co.jp"
    mnode.vm.network "private_network", ip: "192.168.56.60"
    mnode.vm.network "public_network", bridge: "enp0s31f6"
    mnode.vm.synced_folder "./shared", "/vagrant"
  end
  config.vm.define "cnode01" do |cnode01|
    cnode01.vm.box = "generic/rocky8"
    cnode01.vm.box_version = "4.2.8"
    cnode01.vm.hostname = "cnode01.prometech.co.jp"
    cnode01.vm.network "private_network", ip: "192.168.56.61"
    cnode01.vm.network "public_network", bridge: "enp0s31f6"
    cnode01.vm.synced_folder "./shared", "/vagrant"
  end
  config.vm.define "cnode02" do |cnode02|
    cnode02.vm.box = "generic/rocky8"
    cnode02.vm.box_version = "4.2.8"
    cnode02.vm.hostname = "cnode02.prometech.co.jp"
    cnode02.vm.network "private_network", ip: "192.168.56.62"
    cnode02.vm.network "public_network", bridge: "enp0s31f6"
    cnode02.vm.synced_folder "./shared", "/vagrant"
  end
end
