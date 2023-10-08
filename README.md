# LOG8415E

In this assignment we were required deploy a flask application on each EC2 instance launched. The flask application's task is to upon receiving a request provide the id of the EC2 instance handling the request. This way  we can ensure that the Load Balancer and the clusters work as intended.

## Instructions to run the code

- A Linux operating system is **REQUIRED**
- Clone repo from [Github](https://github.com/danieljohannsson/LOG8415E)
- Download [Docker](https://www.docker.com/get-started/)
- The following values need to be stored in `~/.aws/credentials`: 
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY 
  - AWS_SESSION_TOKEN

Once you've completed the above steps, locate the file named "scripts.sh" and then run the following commands:

```bash
#!/bin/bash

# Building Docker
sudo docker build -t 1st-assign-img .

# Running Docker passing the credential use your's credential file path
sudo docker run -v $HOME/.aws/credentials:/root/.aws/credentials:ro 1st-assign-img

This builds and runs our docker image which in turn copies over the files and installs the dependencies, as well as running the python Main. Now the clusters are being setup and should be up and running in a few minutes.
