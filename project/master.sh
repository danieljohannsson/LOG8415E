#!/bin/bash

# Install dependencies
apt-get update
apt-get install libncurses5 libaio1 libmecab2 sysbench -y

# Download and install the MySQL Cluster Manager
cd /home/ubuntu
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb

# Configure the MySQL Cluster Manager and the MySQL Cluster Data Nodes  
mkdir /var/lib/mysql-cluster
echo "
[ndbd default]
NoOfReplicas=3	

[ndb_mgmd]
hostname=ip-172-31-64-5.ec2.internal
NodeId=1
datadir=/var/lib/mysql-cluster 	

[ndbd]
hostname=ip-172-31-64-6.ec2.internal 
NodeId=2			
datadir=/usr/local/mysql/data

[ndbd]
hostname=ip-172-31-64-7.ec2.internal 
NodeId=3			
datadir=/usr/local/mysql/data

[ndbd]
hostname=ip-172-31-64-8.ec2.internal 
NodeId=4			
datadir=/usr/local/mysql/data

[mysqld]
hostname=ip-172-31-64-5.ec2.internal
NodeId=11
" > /var/lib/mysql-cluster/config.ini

# Add the instructions for systemd to start, stop and restart ndb_mgmd
echo "
[Unit]
Description=MySQL NDB Cluster Management Server
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndb_mgmd -f /var/lib/mysql-cluster/config.ini
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ndb_mgmd.service

# Reload systemd manager, enable ndb_mgmd and start ndb_mgmd
systemctl daemon-reload
systemctl enable ndb_mgmd
systemctl start ndb_mgmd

# Download MySQL Server
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
mkdir install
tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

# Install MySQL Server
dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb

# Configure installation to avoid using MySQL prompt
debconf-set-selections <<< 'mysql-cluster-community-server_7.6.6 mysql-cluster-community-server/root-pass password root'
debconf-set-selections <<< 'mysql-cluster-community-server_7.6.6 mysql-cluster-community-server/re-root-pass password root'

# Install the rest of the packages
dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

# Configure client to connect to the master node
echo "
[mysqld]
ndbcluster                   

[mysql_cluster]
ndb-connectstring=ip-172-31-64-5.ec2.internal 
" > /etc/mysql/my.cnf

# Restart MySQL Server
systemctl restart mysql
systemctl enable mysql

# Download Sakila database
cd /home/ubuntu
wget https://downloads.mysql.com/docs/sakila-db.tar.gz -O /home/ubuntu/sakila-db.tar.gz
tar -xvf /home/ubuntu/sakila-db.tar.gz -C /home/ubuntu/

# Upload Sakila database to MySQL
mysql -u root -proot -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;"
mysql -u root -proot -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;"

# Create file for authorizing proxy
cat > authorizeUser.sql << EOF
CREATE USER 'root'@'172.31.64.4' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.31.64.4';
EOF

# Authorize user to connect from proxy
mysql -u root -proot -e "SOURCE /home/ubuntu/authorizeUser.sql;"

# Benchmark using Sysbench and insert data into /home/ubuntu/benchmark.txt
# Using table size of 80 000, 6 threads and maximum time of 60 seconds
sysbench oltp_read_write --table-size=80000 --mysql-db=sakila --mysql-user=root --mysql-password=root prepare
sysbench oltp_read_write --table-size=80000 --threads=6 --time=60 --max-requests=0 --mysql-db=sakila --mysql-user=root --mysql-password=root run > /home/ubuntu/benchmark.txt
sysbench oltp_read_write --mysql-db=sakila --mysql-user=root --mysql-password=root cleanup