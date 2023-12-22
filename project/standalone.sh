#!/bin/bash

# Install MySQL Server and Sysbench
apt-get update
apt-get install mysql-server sysbench -y

# Download Sakila database 
wget https://downloads.mysql.com/docs/sakila-db.tar.gz -O /home/ubuntu/sakila-db.tar.gz
tar -xvf /home/ubuntu/sakila-db.tar.gz -C /home/ubuntu/

# Upload Sakila database to MySQL
mysql -u root -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;"
mysql -u root -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;"

# Benchmark using Sysbench and insert data into /home/ubuntu/benchmark.txt
# Using table size of 80 000, 6 threads and maximum time of 60 seconds
sysbench oltp_read_write --table-size=80000 --mysql-db=sakila --mysql-user=root prepare
sysbench oltp_read_write --table-size=80000 --threads=6 --max-time=60 --max-requests=0 --mysql-db=sakila --mysql-user=root run > /home/ubuntu/benchmark.txt
sysbench oltp_read_write --mysql-db=sakila --mysql-user=root --my-sql-password=root cleanup

