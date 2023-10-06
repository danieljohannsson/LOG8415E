from datetime import datetime, timedelta
import boto3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    cloudwatch = boto3.client('cloudwatch', region_name = "us-east-1")


    # Selected metrics and stat using the following format: 'MetricName': 'Stat'
    metrics_stat = {
        'HTTPCode_ELB_4XX_Count': 'Sum', 
        'HTTPCode_ELB_5XX_Count': 'Sum', 
        'RequestCountPerTarget': 'Sum', 
        'TargetResponseTime': 'Average',
        'HTTPCode_Target_2XX_Count': 'Sum', 
        'HTTPCode_Target_4XX_Count': 'Sum',
    }

    # creating metric queries
    def create_queries():
        metric_queries = []
        for id, metric in enumerate(metrics_stat.keys()):
            namespace_raw = cloudwatch.list_metrics(MetricName=metric)
            namespace = namespace_raw['Metrics'][0]['Namespace']
            metric_queries.append({
                    'Id': f'metric_{id}',
                    'MetricStat': {
                        'Metric': {'MetricName':metric, 'Namespace':namespace},
                        'Period': 30,
                        'Stat': metrics_stat[metric]
                    }
                })

        # Launching the queries
        response = cloudwatch.get_metric_data(
            MetricDataQueries=metric_queries,
            StartTime=datetime.utcnow() - timedelta(minutes=30),
            EndTime=datetime.utcnow()
        )

        data_cluster = response["MetricDataResults"]

        # visualizing the query results
        print(data_cluster)

        return 



    create_queries()
    return