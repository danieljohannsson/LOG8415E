import flask
import boto3
import json
import os

# cat ~/.aws/credentials
os.environ['AWS_ACCESS_KEY_ID'] = ' ASIA4GAOEMH6RTCSLUN7'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'Rtkz4cCIUCp+H9ubINheX6ms/e2wV8ErksMFHzuQ'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEEUaDLkfiW1wPZNAXd6WESLXAZb4AL9sF87W9TGDZRf8WFb42sb3c1vMl6yNa+4vFZ9uTrNJvO8vlGpoGPsLAShXn2fSIM63r3uuIpApLnGwqVDPoCn4lH6QPmfJgT26AKYP7mA9lerKuycosON5Cx14z67Hp9SfqbbTo8N2vEjui93FYNGsUM/vp/hbWljlSxLJHfG5uML9Q7kb907blfMrF/g9Yh2V/AgJn66qyVJ/iIqzMcaWjbLmJA54i1sx6Px9OiANswhEU+thL+rU2E2lqV69uLvRii53573ap4T/3H+fmwUdNalVKNDygqgGMi0f+1SXMob1qP2H9q1Lpmn46H6s8g18FkOpTuFi1TLDPjeWuogdFRmX+E8jc2I='

ecs_client = boto3.client('ecs', region_name = "us-east-1")

response = ecs_client.create_cluster(
    clusterName='MyCluster'
)

# print(response['cluster']['clusterArn'])

print(json.dumps(response, indent=4))

# Create key-pair



# Registering EC2 instance
"""
ec2_client = boto3.client('ec2')

response = ec2_client.run_instances(
    ImageId='ami-0abcdef1234567890',  # replace with your AMI ID
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-key-pair',  # replace with your key pair name
    SubnetId='subnet-0abcdef1234567890',  # replace with your subnet ID
)

instance_id = response['Instances'][0]['InstanceId']
print(instance_id)
"""

# Initialize an EC2 client
ec2_client = boto3.client('ec2', region_name = "us-east-1")

# Define the name for your new key pair
key_pair_name = 'my-key-pair'

try:
    # Create the key pair
    response = ec2_client.create_key_pair(KeyName=key_pair_name)

    # Extract and print the private key (you should save this securely)
    private_key = response['KeyMaterial']
    print(f"Key pair created successfully. Private Key:\n{private_key}")

    # You should save the private key to a secure location
    # and make sure to set appropriate file permissions
    with open(f'{key_pair_name}.pem', 'w') as key_file:
        key_file.write(private_key)

except Exception as e:
    print(f"An error occurred: {str(e)}")
