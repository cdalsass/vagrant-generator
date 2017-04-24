# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.network "forwarded_port", guest: 80, host: 8080
#  config.vm.box = "./base/jf-base.box"
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "bootstrap.sh" 
  config.vm.box_check_update = true
end
