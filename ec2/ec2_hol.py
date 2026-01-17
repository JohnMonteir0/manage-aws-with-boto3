"""
Script to manage AWS EC2 instances using Boto3
"""
# import statemets
import boto3

# create ec2 resource and instance name
ec2 = boto3.resource('ec2', region_name='us-east-1')
instance_name = 'dct-ec2-hol'

# store instace id
instace_id = None

# Chceck if instance which you are trying to create already exists
# and only work with an instance that hasn't been terminated
instances = ec2.instances.all()
instance_exists = False

for instance in instances:
    for tag in instance.tags:
        if tag['Key'] == 'Name' and tag['Value'] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(f"An instance named '{instance_name} with id '{instance_id}' already exists.")
            break
        if instance_exists:
            break


if not instance_exists:
    # Launche a new EC2 instance if it hasn't already been created
    new_instance = ec2.create_instances(
            ImageId='ami-07ff62358b87c7116',
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',
            KeyName='Study',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]

        )
    instance_id = new_instance[0].id
    print(f"Instance named '{instance_name} with id '{instance_id}' created.")

# Stop an instance
# ec2.Instance(instance_id).stop()
# print(f"Instance '{instance_name}-{instance_id}' stopped.")

# Start an instance
# ec2.Instance(instance_id).start()
# print(f"Instance '{instance_name}-{instance_id}' stared.")

# Terminate an instance
ec2.Instance(instance_id).terminate()
print(f"Instance '{instance_name}-{instance_id}' has been terminated.")

