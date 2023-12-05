#!/bin/bash

#Dowlnoad and install mysql
sudo apt-get -y update;
sudo apt-get install mysql-server;
sudo mysql_secure_installation;

#Download and install sakila database
cd ~
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvf sakila-db.tar.gz
rm sakila-db.tar.gz

mysql -u root -e "
SOURCE ~/sakila-db/sakila-schema.sql;
SOURCE ~/sakila-db/sakila-data.sql;
"
rm ~/sakila-db.tar.gz

#Download and install sysbench
sudo apt-get install sysbench;