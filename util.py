import boto3

# creating custom vpc, check necessity
def create_vpc(ec2_client):
    return ec2_client.create_vpc(CidrBlock='10.0.0.0/16')['Vpc']['VpcId']

# TO-DO: create custom subnet for the custom vpc 

# fetching subnet id
def fetch_subnet(ec2_client, vpc_id):
    response = ec2_client.describe_subnets(
                        Filters=[{
                            'Name': 'vpc-id',
                            'Values': [vpc_id]
                        }])
    print(response)
    return response['Subnets'][0]['SubnetId']

# fetching vpcs and subnets id for instance, sg and load balancer
def fetch_vpcs_subnets_ids(ec2_client):
    vpc1_id = create_vpc(ec2_client)
    subnet1_id = fetch_subnet(ec2_client, vpc1_id)
    return vpc1_id, subnet1_id

# creating security group
def create_sg(ec2_client, vpc1_id, vpc2_id=None, sc1_name='cluster1', sc2_name='cluster2'):
    sg1_id = ec2_client.create_security_group(
                        Description='1st cluster security group',
                        GroupName=sc1_name,
                        VpcId=vpc1_id)
    return sg1_id