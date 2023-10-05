import boto3

def EC2_instances(subnets, ec2_client):
    ec2_client = boto3.client('ec2')
    amiId = 'ami-053b0d53c279acc90'
    instanceID = []
    
    def create_key_pair(KPName):
        ec2_client.create_key_pair(KeyName=KPName)
        return KPName
    
    # open instance script
    def launch_script():
        with open("./lab1/flask/instanceScript.sh") as file:
            script = file.read()
        return script
    
    # ec2 instance launcher
    def launch_instance(Itype, subnet, KeyName):
        response = ec2_client.run_instances(
                    ImageId=amiId,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=Itype,
                    KeyName=KeyName,
                    SubnetId=subnet,  
                    UserData=launch_script()
        )
        return response['Instances'][0]['InstanceId'] 
    

    def launch_instances(type, number, KPName):
        for i in range(number):
            instanceID.append(launch_instance(type,subnets[i], KPName))
    
    KPName=create_key_pair("MyKey2")
    launch_instances("t2.large", 4, KPName)
    launch_instances("m4.large", 5, KPName)
    return instanceID

def attach_instances(tg1, tg2, elb_client, cluster, instancesIds,port=80):
    elb_client = boto3.client('elbv2')
   
    if cluster == 1:
        elb_client.register_targets(
            TargetGroupArn = tg1,
            Targets=[{'Id': instancesIds[0], 'Port':port}, {'Id': instancesIds[1], 'Port':port},
                        {'Id': instancesIds[2], 'Port':port}, {'Id': instancesIds[3], 'Port':port}
                    ]
        )
    else:
        elb_client.register_targets(
            TargetGroupArn = tg2,
            Targets=[{'Id': instancesIds[4], 'Port':port}, {'Id': instancesIds[5], 'Port':port},
                        {'Id': instancesIds[6], 'Port':port}, {'Id': instancesIds[7], 'Port':port}, {'Id': instancesIds[8], 'Port':port}
                    ]
        )
