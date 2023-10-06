#!/bin/bash

apt-get update;
apt-get install cloud-utils;
apt-get -y install python3-pip;
pip3 install flask;
pip3 install ec2-metadata;
python3 -c "from flask import Flask
from ec2_metadata import ec2_metadata
app = Flask(__name__)

@app.route('/')
def route_default():
	return ec2_metadata.instance_id

@app.route('/1')
def route1():
	return ec2_metadata.instance_id

@app.route('/2')
def route2():
	return ec2_metadata.instance_id

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)";