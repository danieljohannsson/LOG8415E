import boto3

def EC2_instances(avZones, ec2_client, sgId):
    instanceIds = []
    amiId = 'ami-053b0d53c279acc90' #Os image that will be used in the vm

    # creates key pair and saves the secret key locally
    def create_key_pair(KPName):
        key = ec2_client.create_key_pair(KeyName=KPName)
        private_key = key['KeyMaterial']
        with open(f'{KPName}.pem', 'w') as key_file:
            key_file.write(private_key)
        return KPName
    
    # open and load the instance bash script into variable script
    def launch_script():
        with open("instanceScript.sh", "r") as file:
            script = file.read()
        return script
    
    # ec2 instance launcher
    def launch_instance(KPName, Itype, avZone):
        response = ec2_client.run_instances(
                    ImageId=amiId,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=Itype,
                    KeyName=KPName,
                    Placement={
                        'AvailabilityZone': avZone,
                    },
                    SecurityGroupIds=[sgId],
                    UserData=launch_script()         # passing the loaded bash script to the instance
        )
        return response['Instances'][0]['InstanceId']

    # launch the diffent set of instances
    def launch_cluster(type, number):
        for i in range(number):
            instanceIds.append(launch_instance(KPName, type, avZones[i]))

    
    # creating key pair and lauching the instances
    KPName = create_key_pair('1st-assign-key3')
    launch_cluster('m4.large', 5)
    launch_cluster('t2.large', 4)
    return  instanceIds, KPName

def attach_instances(tg1, tg2, elb_client, instancesIds, port=80):
        
    elb_client.register_targets(
        TargetGroupArn = tg1,
        Targets=[{'Id': instancesIds[0], 'Port':port}, {'Id': instancesIds[1], 'Port':port},
                    {'Id': instancesIds[2], 'Port':port}, {'Id': instancesIds[3], 'Port':port},
                    {'Id': instancesIds[4], 'Port':port}
                ]
    )

    elb_client.register_targets(
        TargetGroupArn = tg2,
        Targets=[{'Id': instancesIds[5], 'Port':port}, {'Id': instancesIds[6], 'Port':port},
                 {'Id': instancesIds[7], 'Port':port}, {'Id': instancesIds[8], 'Port':port},
                ]
    )
    
    return