#!/bin/bash

# Install Python, Pip and Git
apt-get update;
apt-get install python3 python3-pip git -y;

# Install Python libraries needed to run application
pip install pymysql pandas;

cd /home/ubuntu;

cat > vockey.pem << EOF
-----BEGIN RSA PRIVATE KEY-----
your .pem
-----END RSA PRIVATE KEY-----
EOF
# Python script used on the proxy to run SQL queries on the SQL cluster
cat > proxy.py << EOF
import pymysql
import pandas as pd

master_ip = '172.31.64.5'


def create_connection_to_db(ip_adress):
    print('Querying ' + ip_adress)

    connection = pymysql.connect(
        host=ip_adress,
        user='root',
        password='root',
        db="sakila",
        port=3306,
        autocommit=True
    )
    print('Query !')
    
    return connection

def run_direct_hit():
    connection = create_connection_to_db(master_ip)
    data = pd.read_sql_query('SELECT * FROM actor;', connection)
    connection.close()
    
    return data

if __name__ == "__main__":
    print('running direct hit')
    print(run_direct_hit())
EOF
