from flask import Flask
import boto3
import json
import os

# cat ~/.aws/credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'ASIA5ABAG7YKPRFGBXQE'
os.environ['AWS_SECRET_ACCESS_KEY'] = '0RdosbV53ZAAhjazmdaIfkiQU6d31TGcXBWmtnai'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEEMaDDF/jH1A2LXuIlLJ0SLYAXnDvLsqJkcWECC/R1O++//SwPpECskS453s4c0SndrbHuu4bH/mbNRZIQMiNr9FguCDOxEqDtA3VEMJNtfUH0tr0WZpkT2Q2giPwCc4fn2rl9jqhrTHbq5zpzcG8Nre9NWRbgFG8JVrRPXItjhfjK+sgpEkfqj7gXf7OS0w5kgu8ihMyeg8Xt1hqrw+DK8ShR4x0kQaA3ky/vnc0q2aeQfZw3JM+ow8QDMuDVM5SOT+6qv7qzcoA3cL1rw/fcjC3M9fZZQgqy60kNYg+6W/t5rYMnSC/VFPECj5xIKoBjItbTIOA61V0Ic1+mJlcMj1OODiyiElb21yIdz3gd4wL8nu0ZpdjdvZpcKZD2k4'

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
