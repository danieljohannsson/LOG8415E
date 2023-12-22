import time
import boto3
import instance_builder

security_group_names = ['proxy_sg', 'cluster_sg', 'standalone_sg']
instanceIds = []
sgIds = []

# creating proxy
def create_proxy(client):
    print('Creating proxy...')
    security_group_id = instance_builder.create_security_group(client, security_group_names[0], 'For proxy.')
    proxy = instance_builder.create_instances(client,'t2.large', security_group_id, '172.31.64.4', 'proxy')
    instanceIds.append(proxy['Instances'][0]['InstanceId'])
    sgIds.append(security_group_id)

# creating cluster database
def create_cluster(client):
    print('Creating cluster...')
    security_group_id = instance_builder.create_security_group(client, security_group_names[1], 'For SQL cluster.')
    master = instance_builder.create_instances(client,'t2.micro', security_group_id, '172.31.64.5', 'master')
    instanceIds.append(master['Instances'][0]['InstanceId'])
    sgIds.append(security_group_id)

    for i in range(3):
        ip_address = '172.31.64.' + str(6+i)
        instance_name = 'slave_' + str(i + 1)
        slave = instance_builder.create_instances(client,'t2.micro', security_group_id, ip_address, instance_name)
        instanceIds.append(slave['Instances'][0]['InstanceId'])

# creating standalone database
def create_standalone(client):
    print('Creating standalone database...')
    security_group_id = instance_builder.create_security_group_standalone(client)
    standalone_server = instance_builder.create_instances(client,'t2.micro', security_group_id, '172.31.64.9', 'standalone')
    instanceIds.append(standalone_server['Instances'][0]['InstanceId'])
    sgIds.append(security_group_id)

#Starting standale server, cluster and proxy
if __name__ == '__main__':
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    waiter = ec2_client.get_waiter('instance_terminated')

    create_standalone(ec2_client)
    create_cluster(ec2_client)
    create_proxy(ec2_client)
    
    while (input('Press enter to terminate instances...') != ''):
        continue
    
    print('Terminating instances...')
    instance_builder.shut_down_instances(ec2_client, instanceIds)
    
    waiter.wait(InstanceIds=instanceIds)
    print('All terminated')
    
    instance_builder.delete_security_group(ec2_client, sgIds)
    print('Security groups deleted')
    