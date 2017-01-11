#!/bin/bash

su vagrant
sudo dnf -y install python3-pip python3-devel redhat-rpm-config gcc nano git mysql-devel wget

# install and configure postgresql
sudo dnf -y install postgresql postgresql-server postgresql-contrib postgresql-devel
sudo postgresql-setup initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo -u postgres createuser -s vagrant
sudo -u postgres createdb -U postgres --locale=en_US.utf-8 -E utf-8 -O vagrant phoenix -T template0

# install and configure rabbitmq
sudo dnf -y install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# install and configure memcached
sudo dnf -y install memcached libmemcached-devel
sudo systemctl enable memcached.service
sudo systemctl start memcached.service

# install and configure redis
sudo dnf -y install redis
sudo systemctl enable redis.service
sudo systemctl start redis.service

# install cloud foundry cli
wget -q https://cli.run.pivotal.io/stable?release=redhat64 -O /tmp/cf-cli-installer.rpm
sudo rpm -i /tmp/cf-cli-installer.rpm

# install travis-ci cli
sudo dnf -y install ruby ruby-devel
gem install travis --no-rdoc --no-ri

# install requirements for Pillow
sudo dnf -y install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel

# create python3 virtual environment
pyvenv /home/vagrant/dj_pyvenv
source /home/vagrant/dj_pyvenv/bin/activate
pip3 install -r /vagrant/requirements.txt

# vagrant user default into virtual environment
echo "source /home/vagrant/dj_pyvenv/bin/activate" >> /home/vagrant/.bashrc
echo "source /vagrant/scripts/envionments.sh" >> /home/vagrant/.bashrc
echo "cd /vagrant" >> /home/vagrant/.bashrc
