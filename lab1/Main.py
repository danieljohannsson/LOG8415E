import boto3
import util
import load_balancer
import ec2_instances
import web_requests
import time
import benchmarks_analysis

def main():
    # Initializing clients for EC2 and ELBv2 services
    ec2_client = boto3.client('ec2', region_name = "us-east-1")
    elb_client = boto3.client('elbv2', region_name = "us-east-1")

    # Declaring Availability zones
    avZones = ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e']

    # create security zone
    sgId = util.create_sg(ec2_client)
    print("client connected")

    # fetching subnets
    subnets = util.fetch_subnet(ec2_client, avZones)

    # Launch 9 instances
    instancesIds, KPName = ec2_instances.EC2_instances(avZones, ec2_client, sgId)
    print('instances launched')
    time.sleep(60)

    # creating the load balancer, target groups, listener and routing rules
    lbArn, tg1Arn, tg2Arn, lbDNS = load_balancer.create_lb_listener(subnets, ec2_client, elb_client, sgId)
    print('lb created')
    time.sleep(120)

    # attaching instances to the target groups
    ec2_instances.attach_instances(tg1Arn, tg2Arn, elb_client, instancesIds)
    print("instances attached")
    time.sleep(180)
    
    

    # sending get requests
    print('requesting')
    web_requests.requests_main(lbDNS)

    print('Requests done!')
    
    # Realizing benchmark analysis and printing it
    time.sleep(240)
    results = benchmarks_analysis.main()
    pprint.pprint(results, indent=4)

    # terminating resources
    util.shut_down_instances(ec2_client, instancesIds)
    util.shut_down_load_balancer(elb_client, lbArn, tg1Arn, tg2Arn)
    time.sleep(120)
    util.delete_security_group(ec2_client, sgId)
    util.delete_key_pair(ec2_client, KPName)

    print('All terminated')
    return

main()
