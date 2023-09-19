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