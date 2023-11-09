#!/bin/bash

# Add Docker's official GPG key:
sudo apt-get -y update;
sudo apt-get -y install ca-certificates curl gnupg;
sudo install -m 0755 -d /etc/apt/keyrings;
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg |sudo gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg;
sudo chmod a+r /etc/apt/keyrings/docker.gpg;
# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null;
sudo apt-get -y update;
# Installing Docker and Docker compose plugin
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin;
# creating docker compose
cat > docker-compose.yml << EOL
services:
  1st_pythonapp:
    container_name: 1stContainer
    build: ./
    command: python ./server.py 5000
    ports:
       - "5000:5000"
    
  2nd_pythonapp:
    container_name: 2ndContainer
    build: ./
    command: python ./server.py 5001
    ports:
       - "5001:5001"

EOL
# Creating dockerfile
cat > dockerfile << EOL
FROM python:3.10

# Copying files to the docker container
COPY ./server.py .

# Installing dependencies
RUN pip install Flask
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install transformers[torch]
EOL
# Creating server.py
cat > server.py << EOL
from flask import Flask, jsonify
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import random
import string
import argparse

app = Flask(__name__)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

def generate_random_text(length=50):
    letters = string.ascii_lowercase + ' '
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/run_model', methods=['POST'])
def run_model():
    input_text =  generate_random_text()
    
    inputs = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)
    probabilities_list = probabilities.tolist()[0]

    return jsonify({"input_text": input_text, "probabilities": probabilities_list})

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, help='server port')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)
EOL
# Launching containers 
sudo docker compose -p workers up --build;