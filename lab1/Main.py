import boto3
import util
import load_balancer
import ec2_instances
import web_requests
import time
import socket
import benchmarks_analysis

def main():
    ec2_client = boto3.client('ec2')
    elb_client = boto3.client('elbv2')
    avZones = ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e']
    sgId = util.create_sg(ec2_client)
    print("client connected")

    subnets = util.fetch_subnet(ec2_client, avZones)
    instancesIds = ec2_instances.EC2_instances(avZones, ec2_client, sgId)
    print('instances launched')
    time.sleep(60)

    lbArn, tg1Arn, tg2Arn, lbDNS = load_balancer.create_lb_listener(subnets, ec2_client, elb_client, sgId)
    print('lb created')
    time.sleep(120)
    ec2_instances.attach_instances(tg1Arn, tg2Arn, elb_client, instancesIds)
    print("instances attached")
    time.sleep(180)
    try:
        print('requesting')
        web_requests.requests_main(lbDNS)

        print('Requests done!')

    except:
        print('Problems')
    
    
    #benchmarks_analysis.main()

    print('All terminated')
    return

main()