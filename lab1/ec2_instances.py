import boto3

def EC2_instances(tg1, tg2, subnets, ec2_client, elb_client):
    ec2_client = boto3.client('ec2')
    elb_client = boto3.client('elbv2')
    amiId = 'ami-03a6eaae9938c858c'

    
    def create_key_pair(KPName):
        ec2_client.create_key_pair(KeyName=KPName)
        return KPName
    
    # open instance script
    def launch_script():
        with open("instanceScript.sh", "r") as file:
            script = file.read()
        return script
    
    # ec2 instance launcher
    def launch_instance(KPName, Itype, subnet):
        response = ec2_client.run_instances(
                    ImageId=amiId,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=Itype,
                    KeyName=create_key_pair(KPName),
                    SubnetId=subnet,  
                    UserData=launch_script()
        )
        return response['Instances'][0]['InstanceId']
    
    def attach_instances(type, cluster, port=80):
        ec2_resource = boto3.resource('ec2')
        instancesIds = []
        flag = 1
        if cluster == 1:
            for i in range(0, len(subnets)):
                instancesIds.append(launch_instance(f'kp_Cluster-{cluster}_Instance-{i+1}', type, subnets[i]))
            
            while(flag):
                for i in instancesIds:
                    if ec2_resource.Instance(i).state['Name'] != 'running':
                        flag = 1
                        break
                    else:
                        flag = 0
            
            elb_client.register_targets(
                TargetGroupArn = tg1,
                Targets=[{'Id': instancesIds[0], 'Port':port}, {'Id': instancesIds[1], 'Port':port},
                         {'Id': instancesIds[2], 'Port':port}, {'Id': instancesIds[3], 'Port':port},
                         {'Id': instancesIds[4], 'Port':port}
                        ]
            )
        else:
            for i in range(0, len(subnets)-1):
                instancesIds.append(launch_instance(f'kp_Cluster-{cluster}_Instance-{i+1}', type, subnets[i]))

            while(flag):
                for i in instancesIds:
                    if ec2_resource.Instance(i).state['Name'] != 'running':
                        flag = 1
                        break
                    else:
                        flag = 0

            elb_client.register_targets(
                TargetGroupArn = tg2,
                Targets=[{'Id': instancesIds[0], 'Port':port}, {'Id': instancesIds[1], 'Port':port},
                         {'Id': instancesIds[2], 'Port':port}, {'Id': instancesIds[3], 'Port':port},
                        ]
            )
        
        return instancesIds

    C1_ids = attach_instances('t2.large', 1)
    C2_ids = attach_instances('m4.large', 2)
    return  C1_ids, C2_ids