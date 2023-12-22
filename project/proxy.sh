#!/bin/bash

# Install Python, Pip and Git
apt-get update;
apt-get install python3 python3-pip git -y;

# Install Python libraries needed to run application
pip install pymysql pandas;

cd /home/ubuntu;

cat > vockey.pem << EOF
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2Pzow8r6d2mHv8tzk64iYycNdEfGsyv+kkCm6USt+p2FvGmS
M7xL+RgmQl4eZ4fLYhAMAuNMl8MLOBJ9AECJsBS2bqu/c6NOi8zHHqpEDEFdMRDR
4Vi+yvaIvVKiTyXn6N0A0STBKPrgJQ1pR1hraB6a0OO2HI+MqXgK3rl3bmgntRKA
yAlbLjvKWZLf4f1K5/fHYeb6F9FmkLTLYNrttPbWrUqm6TCBmS3uCfSykDbGNLYk
hEwVe4qi2xzCiqGSk9m9t/8tXL4DrIoX1CmgDGCWZsC3qp9x5PieeSIi7VlkIWIW
OWWBWbT3fKTHHGZZELHDOV+m2yNi9Lo9NRkn7wIDAQABAoIBAQDGhd2QBM1TI0IH
v+RmYRMlFD3C/UhV9RJcTLppAWULvcL1tsEEhGod5HJcli/LGPqDJZtXqQ4Sa2iA
TKoA6QsQBmNCre/jpK3gSeKDs9O+Qq84jOL5AXDN0PEaBdhqAYxECK8OqknvbFhW
jgacN9FM2XNbWnrrdoqDIkkPrTAP2ZqVGMIkRBGhT9jyYv6GMjqn+UTp48x6SqZ0
J+X1D4b/JVFADW4oB0o/WWNgmFyydikl2lzwh7FBK9EGf5gXm0kvGjrIjslSe5t/
PTbglMotsUOLE4c5284+NoqwJcOBf9PqhRqEdz3D5b9Ym0UpmnzKxt7lr4PWsS9M
Kf5IR08BAoGBAP9IzUfA8RkpOCWNLsgqk7a7ehZs0mrFPCNgOP1SjYpYYPDZ00Yp
qcj89/3PSGPyQqn/kHm71EN2GBQDqM9mhilyVtgF++v1uuo8pyE00muKZY9er6CV
Zb48DRSBFiwJ5clGiEjg2nPbmzc/4Vt3LI5YlcFcSFdCfehEjXqV0A9fAoGBANmY
n/qRo7nrL5fPPkcnebJkfX/lTBIL0LmdG2hInhTpJ1UvqMZ50xWfgiEHoL1ficRO
i1aB8zgB+eAFUmocM9zxrZ5U1AJygG0+dawAMRM6pd77ZhhKHslOYs7my8T9U+KJ
3MCQlfkfRKvaarFE1rY8uM+Q/39jaOUYhCe/rQFxAoGAOz1Bpaz4RcZy6QPiH0EC
Fh1bL2kBSxWJ5wulLePCRKBNnpZtmJKCe8l4IsW/HrJRFfHgLN+RWjZFUB+pRLed
2nBWBrscwpy7Sy/X+LSxP5NWDfcC+liwy3xT7LYn1wBU+mgLqB3Fk60aT6/bM8Zr
6HxWBBDOGLGtVgDSc+ff6DECgYEAmbZPjNpFJpkVTdCA1hL0zShf33FDg5wFHpn1
On3R7kOmHW9Fcq+shaHgcyTIT/6le59gnwO9pNsAgVhBF+REXtf7JdYWzoPEZWey
CIc6I7NSaWp+fLofdWWCN1aiq82o7GcnIoEA8LM994ibxg4y/xl2FGsBkiPPfccL
1Gh69oECgYANfRuEqkUpcOcx7rhxBu5OTXWaLeSAC4aykewIRbmY9k2jfGsV6C3H
HnX1S7t95YRWrb/N2s0/aj7REAsqDPDY6whJCoeBhUr4Aa7vH67U0mLSvMwgI4Md
8kgC41rjxuNEW/tZFXlDPdUVWOLuajxzBfayodksDitmJoF8rQ/adQ==
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