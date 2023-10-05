import boto3
import util
import load_balancer
import ec2_instances
import web_requests
import time

def main():
    ec2_client = boto3.client('ec2')
    elb_client = boto3.client('elbv2')
    avZones = ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e']
    print("Clients created!")
    subnets = util.fetch_subnet(ec2_client, avZones)

    Instances_ids = ec2_instances.EC2_instances( subnets, ec2_client)
    print('Instances created!')

    lbArn, tg1Arn, tg2Arn, security_groups = load_balancer.create_lb_listener(subnets, ec2_client, elb_client)
    print('LB created!')
    time.sleep(120)

    ec2_instances.attach_instances(tg1Arn, tg2Arn, elb_client, 1, Instances_ids)
    ec2_instances.attach_instances(tg1Arn, tg2Arn, elb_client, 2, Instances_ids)
    print('Attached instances!')
    
    time.sleep(120)
    web_requests.requests_main()


    util.shut_down_instances(ec2_client, Instances_ids)
    util.shut_down_load_balancer(elb_client, lbArn, tg1Arn, tg2Arn)
    time.sleep(120)
    #DELETE SECURITY GROUP
    #DELETE KEYPAIR
    print('All terminated')

    return

main()