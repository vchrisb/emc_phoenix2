#!/bin/bash

su vagrant
sudo dnf -y install python3-pip python3-devel redhat-rpm-config postgresql postgresql-devel gcc nano git mysql-devel wget

# install and configure rabbitmq
sudo dnf -y install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# install and configure memcached
sudo dnf -y install memcached
sudo systemctl enable memcached.service
sudo systemctl start memcached.service

# install cloud foundry cli
wget -q https://cli.run.pivotal.io/stable?release=redhat64 -O /tmp/cf-cli-installer.rpm
sudo rpm -i /tmp/cf-cli-installer.rpm

# install requirements for Pillow
sudo dnf -y install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel

# create python3 virtual environment
pyvenv /home/vagrant/dj_pyvenv
source /home/vagrant/dj_pyvenv/bin/activate
pip3 install -r /vagrant/django/requirements.txt

# vagrant user default into virtual environment
echo "source /home/vagrant/dj_pyvenv/bin/activate" >> /home/vagrant/.bashrc
echo "source /home/vagrant/django/envionments.sh" >> /home/vagrant/.bashrc
echo "cd /home/vagrant/django" >> /home/vagrant/.bashrc