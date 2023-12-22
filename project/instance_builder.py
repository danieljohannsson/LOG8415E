import boto3

# deleting security key
def delete_security_group(ec2_client, sgIds):
    for sgId in sgIds:
        ec2_client.delete_security_group(GroupId=sgId)
    return

# deleting key pair
def delete_key_pair(ec2_client, KPName):
    ec2_client.delete_key_pair(KeyName=KPName)
    return

# terminating instance
def shut_down_instances(ec2_client, ids):
    ec2_client.terminate_instances(
        InstanceIds = ids
    )
    return

# fetching default vpc
def fetch_vpc(ec2_client = None):
    if not ec2_client:
        ec2_client = boto3.client('ec2', region_name = "us-east-1")
    
    return ec2_client.describe_vpcs()['Vpcs'][0]['VpcId']

# creating security group for standalone server
def create_security_group_standalone(client):
    ec2_resource = boto3.resource('ec2', region_name = "us-east-1")
    security_group = ec2_resource.create_security_group(
        GroupName='standalone',
        Description='For standalone server.',
        VpcId=fetch_vpc(client)
    )
    #Adding rules for security group
    client.authorize_security_group_ingress(
        GroupId=security_group.group_id,
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        GroupName='standalone'
    )
        
    return security_group.group_id

# creating security group for cluster and proxy
def create_security_group(client, security_group_name, description):
    ec2_resource = boto3.resource('ec2', region_name = "us-east-1")
    security_group = ec2_resource.create_security_group(
        GroupName=security_group_name,
        Description=description,
        VpcId=fetch_vpc(client)
    )
    #Adding rules for security group
    client.authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='-1',
        FromPort=0,
        ToPort=65535,
        GroupName=security_group_name
    )
        
    return security_group.group_id

# launching script for the instances based on their role
def launch_script(role):
    path = f'{role}.sh'
    with open(path, "r") as file:
        script = file.read()
    return script

# creating EC2 instances
def create_instances(client, instance_type, security_group_id, ip_address, instance_name):
        return client.run_instances(
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            ImageId='ami-0574da719dca65348',
            KeyName='vockeyFinal',
            SecurityGroupIds=[security_group_id],
            SubnetId='subnet-0e3b3bc7324035810',
            UserData=launch_script("slave") if instance_name.startswith("slave") else launch_script(instance_name), 
            PrivateIpAddress=ip_address,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]
        )

