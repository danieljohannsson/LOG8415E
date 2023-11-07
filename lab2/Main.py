import boto3
import time
import util
import subprocess
import web_requests
from lab2.ec2_instances import EC2_instances


def main():
    # Initializing clients for EC2 service
    ec2_client = boto3.client('ec2', region_name = "us-east-1")
    print("client connected")

    # Declaring Availability zones
    avZones = ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e']

    # create security zone
    sgId = util.create_sg(ec2_client)
    print("client connected")

    # Launch 4 workers and 1 orchestrator of type m4 large
    instancesIds, KPName = EC2_instances.EC2_instances(avZones, ec2_client, sgId)
    orchestratorIP = instancesIds[-1][1]

    # run the orchestrator script 
    result = subprocess.run(['sh', './orchestrator.sh'])

    # Sending post requests (5 threads)
    print('requesting')
    web_requests.requests_main(orchestratorIP)
    print('Requests done!')
    
    # terminating resources
    """
    util.shut_down_instances(ec2_client, instancesIds)
    time.sleep(120)
    util.delete_security_group(ec2_client, sgId)
    util.delete_key_pair(ec2_client, KPName)
    """

    print('All terminated')
    return

main()

