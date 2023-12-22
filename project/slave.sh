#!/bin/bash
 
# Download and install MySQL Cluster Data Node
cd /home/ubuntu
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

# Setup with master node
echo "
[mysql_cluster]
ndb-connectstring=ip-172-31-64-5.ec2.internal
" > /etc/my.cnf

# Creating data directory 
mkdir -p /usr/local/mysql/data

# Add the instructions for systemd to start, stop and restart ndb_mgmd
echo "
[Unit]
Description=MySQL Data Node Daemon
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndbd
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ndbd.service

# Reload systemd manager, enable ndb_mgmd and start ndb_mgmd
systemctl daemon-reload
systemctl enable ndbd
systemctl start ndbd