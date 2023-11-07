#!/bin/bash

ip1=$(cat ip1.txt)
ip2=$(cat ip2.txt)
ip3=$(cat ip3.txt)
ip4=$(cat ip4.txt)


cat > orchestrator.sh << EOL
#!/bin/bash

sudo apt-get update;
sudo apt-get -y install python3-pip;
sudo pip3 install flask;
cat > ip.json << EOF
{
	"container1":{
		"ip": "${ip1}",
		"port": "5000",
		"status": "free"
	}
	"container2":{
		"ip": "${ip1}",
		"port": "5001",
		"status": "free"
	}
	"container3":{
		"ip": "${ip2}",
		"port": "5000",
		"status": "free"
	}
	"container4":{
		"ip": "${ip2}",
		"port": "5001",
		"status": "free"
	}
	"container5":{
		"ip": "${ip3}",
		"port": "5000",
		"status": "free"
	}
	"container6":{
		"ip": "${ip3}",
		"port": "5001",
		"status": "free"
	}
	"container7":{
		"ip": "${ip4}",
		"port": "5000",
		"status": "free"
	}
	"container8":{
		"ip": "${ip4}",
		"port": "5001",
		"status": "free"
	}
}
EOF

cat > server.py << EOF
from flask import Flask, jsonify, request
import json
import threading
import time
import requests

app = Flask(__name__)
lock = threading.Lock()
request_queue = []

def send_request_to_container(container_id, container_info, incoming_request_data):
	print(f"Sending request to {container_id} with data: {incoming_request_data}")
	# TO-DO: Send the request
	url = f'http://{container_info.ip}:{container_info.port}'
	response = requests.get(url)
	print(f"Response from {url}: {response.status_code}, {response.text}")
	print(f"Receivde response from {container_id}")

def update_container_status(container_id, status):
	with lock:
		with open("ip.json", "r") as f:
			data = json.load(f)
		data[container_id]["status"] = status
		with open("ip.json", "r") as f:
			json.dump(data, f)
def process_request(incoming_request_data):
	with lock:
		with open("ip.json", "r") as f:
			data = json.load(f)
	free_container = None
	for container_id, container_info in data.items():
		if container_info["status"] == "free":
			free_container = containeri_id
			break
	if free_container:
		update_container_status(free_container, "busy")
		send_request_to_container(free_container, data[free_container], incoming_request_data)
		update_container_status(free_container, "free")
	else:
		request_queue.append(incoming_request_data)
		
@app.route("/new_request", methods=["POST"])
def new_request():
	incoming_request_data = request.json
	threading.Thread(target=process_request, args=(incoming_request_data,)).start()
	return jsonify({"message": "Request received and processing started."})

if __name__ == "__main__":
	app.run(port=80)
EOF

python3 server.py

EOL