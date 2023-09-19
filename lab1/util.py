import boto3

# fetching default vpc
def fetch_vpc(ec2_client = None):
    if not ec2_client:
        ec2_client = boto3.client('ec2')
    
    return ec2_client.describe_vpcs()['Vpcs'][0]['VpcId']

# fetching subnet id
def fetch_subnet(ec2_client, vpc_id):
    response = ec2_client.describe_subnets(
                        Filters=[{
                            'Name': 'vpc-id',
                            'Values': [vpc_id]
                        }])
    return response['Subnets'][0]['SubnetId']

# creating security group
def create_sg(sc1_name='cluster1', sc2_name='cluster2'):
    ec2_resource = boto3.resource('ec2')
    sg1_id = ec2_resource.create_security_group(
                        Description='1st cluster security group',
                        GroupName=sc1_name,
                        VpcId=fetch_vpc())
    return sg1_id