import boto3
import subprocess, pprint

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
    
    # open and load the instance bash script into a string variable
    def launch_script():
        with open("workerScript.sh", "r") as file:
            script = file.read()
        return script
    
    def launch_script_orchestrator():
        with open("orchestratorScript.sh", "r") as file:
            script = file.read()
        return script
    
    # ec2 instance launcher
    def launch_instance(KPName, Itype, avZone, role = 0):
        response = ec2_client.run_instances(
                    ImageId=amiId,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=Itype,
                    KeyName=KPName,
                    SecurityGroupIds=[sgId],
                    UserData=launch_script_orchestrator() if role == 1 else launch_script() # passing the loaded bash script to the instance
        )
        ec2 = boto3.resource('ec2')
        id = response['Instances'][0]['InstanceId']
        instance = ec2.Instance(id)
        instance.wait_until_running()
        instance.reload()
        
        pprint.pprint(instance.public_ip_address)
        return id, instance.public_ip_address

    # launch the diffent set of instances
    def launch_cluster(type, number):
        for i in range(number):
            instanceIds.append(launch_instance(KPName, type, avZones[i]))

    # store ip adress of instances in files
    def storeIpAddresses(instanceIds):
        for i in range(4):
            with open(f"ip{i+1}.txt", "w") as file:
                file.write(instanceIds[i][1])
            

    # creating key pair and lauching the instances
    KPName = create_key_pair('2nd-assign-key')
    launch_cluster('m4.large', 4)

    # store ip adresses of workers
    storeIpAddresses(instanceIds)

    # run the orchestrator script 
    result = subprocess.run(['sh', './orchestrator.sh'])

    # launch orchestrator
    instanceIds.append(launch_instance(KPName, 'm4.large', avZones[0], 1))

    return  instanceIds, KPName
