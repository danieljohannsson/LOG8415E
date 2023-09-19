import boto3
import util

def create_lb_listener():

    elb_client = boto3.client('elbv2')
    vpc = util.fetch_vpc()

    def create_tg(name, VpcId):
    response = elb_client.create_target_group(Name=name, Protocol='HTTP', Port=80, VpcId=VpcId)

    return response['TargetGroups'][0]['TargetGroupArn']


    def launch_lb():
    load_balancer = elb_client.create_load_balancer(
                    Name = 'LoadBalancer',
                    Subnet = ['us-east-1', 'us-east-2'],
                    SecurityGroups=util.create_sg()
                    )

    return load_balancer_dns = load_balancer['LoadBalancers'][0]['LoadBalancerArn']

    def create_rule(listenerArn, route, TGArn, priority):
        elb_client.create_rule(
                ListenerArn = listenerArn,
                Actions = [{
                            'Type': 'forward'
                            'TargetGroupArn': TGArn
                          }]
                Conditions = [{
                            'Field':'path-pattern'
                            'Values':[route]
                             }]
                Priority = priority
        )
        return
    
    tg1Arn = create_tg('cluster1', vpc)
    tg2Arn = create_tg('cluster2', vpc)

    listenerArn = elb_client.create_listener(
                            LoadBalancerArn = create_lb(),
                            Protocol = 'HTTP',
                            Port = 80,
                            DefaultActions = [{
                                            'Type' = 'forward'
                                            'TargetGroupArn' = tg1Arn
                                            'Order' = 1
                                             }]
                    )['Listeners'][0]['ListernerArn']

    route_1 = create_rule(listenerArn, '/1', tg1Arn, 1)
    route_2 = create_rule(listenerArn, '/2', tg2Arn, 2)

    return load_balancer_dns