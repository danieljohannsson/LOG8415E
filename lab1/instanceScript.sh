#!/bin/bash

apt update;
apt -y install python3-pip;
pip3 install flask;
INSTANCEID=$(ec2metadata -i);
python -c "from flask import Flask
app = Flask(__name__)

@app.route("/")
def route_default():
	return '"$INSTANCEID"'

@app.route("/1")
def route1():
	return '"$INSTANCEID"'

@app.route("/2")
def route2():
	return '"$INSTANCEID"'

if __name__ == "__main__":
	app.run()";