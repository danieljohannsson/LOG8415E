import boto3
import util
import load_balancer
import ec2_instances

def main():
    ec2_client = boto3.client('ec2')
    elb_client = boto3.client('elbv2')
    avZones = ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e']
    print("client criado")
    subnets = util.fetch_subnet(ec2_client, avZones)
    lbArn, tg1Arn, tg2Arn, sgId = load_balancer.create_lb_listener(subnets, ec2_client, elb_client)
    print('lb criado')
    C1_ids, C2_ids = ec2_instances.EC2_instances(tg1Arn, tg2Arn, subnets, ec2_client, elb_client)
    print('instancias criadas')
    util.shut_down_instances(ec2_client, C1_ids)
    util.shut_down_instances(ec2_client, C2_ids)
    util.shut_down_load_balancer(elb_client, lbArn, tg1Arn, tg2Arn)
    # util.shut_down_security_group(sgId)
    print('tudo deletado')

    return

main()