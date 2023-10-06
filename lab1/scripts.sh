#!/bin/bash

# Building Docker
sudo docker build -t 1st-assign-img .

# Running Docker passing the credential use your's credential file path
sudo docker run -v $HOME/.aws/credentials:/root/.aws/credentials:ro 1st-assign-img
