#!/bin/bash

sudo apt-get -y update;

wget http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql- cluster-gpl-7.2.1linux2.6-x86_64.tar.gz
tar xvf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc
echo ‘export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc’ > /etc/profile.d/mysqlc.sh
echo ‘export PATH=$MYSQLC_HOME/bin:$PATH’ >> /etc/profile.d/mysqlc.sh
source /etc/profile.d/mysqlc.sh
sudo apt-get update && sudo apt-get -y install libncurses5


sudo apt-get install sysbench;