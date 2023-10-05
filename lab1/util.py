import boto3
import time

# fetching default vpc
def fetch_vpc(ec2_client = None):
    if not ec2_client:
        ec2_client = boto3.client('ec2')
    
    return ec2_client.describe_vpcs()['Vpcs'][0]['VpcId']

# fetching subnet id
def fetch_subnet(ec2_client, avZones):
    subnets = []
    for zone in avZones:
        response = ec2_client.describe_subnets(
                            Filters=[{
                                'Name': 'availabilityZone',
                                'Values': [zone]
                            }])
        subnets.append(response['Subnets'][0]['SubnetId'])
    return subnets

# creating security group
   # Gets the vpc of the current deployment
def create_sg(sc1_name='SG2'):
    ec2_resource = boto3.resource('ec2')
    sg1_id = ec2_resource.create_security_group(
                        Description='1st cluster security group',
                        GroupName=sc1_name,
                        VpcId=fetch_vpc())

    return sg1_id.group_id


def shut_down_instances(ec2_client, ids):
    ec2_client.terminate_instances(
        InstanceIds = ids
    )
    return

def shut_down_load_balancer(elb_client, lbArn, tg1Arn, tg2Arn):
    elb_client.delete_load_balancer(LoadBalancerArn=lbArn)
    time.sleep(60)
    elb_client.delete_target_group(TargetGroupArn=tg1Arn)
    elb_client.delete_target_group(TargetGroupArn=tg2Arn)
    return

def shut_down_security_group(ec2_client, security_groups):
    ec2_client.delete_security_group(GroupId=security_groups)
    return

def create_security_group(ec2, vpc_id):
    security_group = ec2.create_security_group(
        Description="security group TP1",
        GroupName="TestSG69",
        VpcId=vpc_id
    )

    #create_outbound_rules(ec2, security_group['GroupId'])
    #create_inbound_rules(ec2, security_group['GroupId'])
    ec2.authorize_security_group_ingress(
            GroupId=security_group['GroupId'],
            IpProtocol='-1',    
            FromPort=80,          
            ToPort=80,       
            CidrIp='0.0.0.0/0' 
        ) 
    return security_group

def create_inbound_rules(ec2, security_group_id):

    ip_permission = [{
        'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }, {
        'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }, {
        'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]

    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=ip_permission)


def create_outbound_rules(ec2, security_group_id):
    ip_permission = [{
        'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }, {
        'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]

    ec2.authorize_security_group_egress(
        GroupId=security_group_id,
        IpPermissions=ip_permission)