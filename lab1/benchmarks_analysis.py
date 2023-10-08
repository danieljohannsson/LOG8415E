from datetime import datetime, timedelta
import boto3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    region_name="us-east-1"
    client = boto3.client('cloudwatch', region_name = region_name)
    namespace = 'AWS/ApplicationELB'
    # Selected metrics and stat using the following format: 'MetricName': 'Stat'
    metric_names_stats = {
        'HTTPCode_ELB_4XX_Count': 'Sum',
        'HTTPCode_ELB_5XX_Count': 'Sum',
        'RequestCountPerTarget': 'Sum',
        'TargetResponseTime': 'Average',
        'HTTPCode_Target_2XX_Count': 'Sum',
        'HTTPCode_Target_4XX_Count': 'Sum'
    }
    period = 5  # in seconds
    time_offset = 30 * 60  # last 30 minutes in seconds

    # Determine the unit based on the metric name
    def get_unit(metric_name):
        if metric_name in ['HTTPCode_ELB_4XX_Count','HTTPCode_ELB_5XX_Count','HTTPCode_Target_2XX_Count','HTTPCode_Target_4XX_Count']:
            return 'Count'
        elif metric_name == 'TargetResponseTime':
            return 'Seconds'  # or whatever unit is appropriate for response time
        else:
            return 'None'  # No unit

    session = boto3.Session(region_name=region_name)
    elbv2_client = session.client('elbv2')

    resp = elbv2_client.describe_target_groups()

    load_balancer = resp['TargetGroups'][0]['LoadBalancerArns'][0]
    target_group1 = resp['TargetGroups'][0]['TargetGroupArn']
    target_group2 = resp['TargetGroups'][1]['TargetGroupArn']

    tgarray1 = target_group1.split(':')
    tgstring1 = tgarray1[-1]

    tgarray2 = target_group2.split(':')
    tgstring2 = tgarray2[-1]

    lbarray = load_balancer.split(':')
    lbstring = lbarray[-1]
    lbarray2 = lbstring.split('/')
    lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    # creating metric queries
    metric_queries = []
    for metric_idx, (metric_name, stat) in enumerate(metric_names_stats.items()):
        for tg_idx, tg in enumerate([tgstring1, tgstring2]):
            # Using indices for generating Id
            id_string = f"m{metric_idx}_tg{tg_idx}"
            metric_queries.append({
                'Id': id_string,
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': [
                            {"Name": "TargetGroup", "Value": tg},
                            {"Name": "LoadBalancer", "Value": lbstring2}
                        ]
                    },
                    'Period': period,
                    'Stat': stat,
                    'Unit': get_unit(metric_name)
                }
            })

    # Launching the queries
    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime.utcnow() - timedelta(seconds=time_offset),
        EndTime=datetime.utcnow()
    )

    # returning for visualizing the query results
    return response["MetricDataResults"]


def instances_metrics(instance_ids):
    region_name = "us-east-1"
    # Client for CloudWatch
    client = boto3.client('cloudwatch', region_name=region_name)
    namespace = 'AWS/EC2'

    # Metric details
    metric_name = 'CPUUtilization'
    stat = 'Average'  
    period = 10
    time_offset = 30 * 60  # last 30 minutes in seconds

    # Creating metric queries
    metric_queries = []
    for index, instance_id in enumerate(instance_ids):
        metric_queries.append({
            'Id': f"cpu_utilization_{index}",
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}]
                },
                'Period': period,
                'Stat': stat,
                'Unit': 'Percent'
            }
        })

    # Fetching the metrics
    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime.utcnow() - timedelta(seconds=time_offset),
        EndTime=datetime.utcnow()
    )

    return response["MetricDataResults"]
