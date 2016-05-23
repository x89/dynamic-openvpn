#!/usr/bin/env python3

import argparse
import boto3
import os
import signal
import subprocess
import time

parser = argparse.ArgumentParser(description='Spin up an EC2 OpenVPN instance.')
parser.add_argument('--ami', help="AMI Image", default="ami-2c37845f")
parser.add_argument('--sg', help="Security Group ID", default="sg-cb0669af")
parser.add_argument('--port', help="OpenVPN Port", default=1250)
args = parser.parse_args()

client = boto3.client('ec2')

response = client.run_instances(
    DryRun=False,
    ImageId=args.ami,
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=[args.sg],
    InstanceType='t2.nano',
    Placement={
        'AvailabilityZone': 'eu-west-1a',
    },
    Monitoring={
        'Enabled': False
    },
    InstanceInitiatedShutdownBehavior='terminate',
)

instance_id = response['Instances'][0]['InstanceId']

print("Starting instance: {0}".format(instance_id))

time.sleep(2)  # Sleep to wait for a public IP

response = client.describe_instances(
    InstanceIds=[
        instance_id
    ]
)

public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print("Public IP for {0} is {1}".format(instance_id, public_ip))

def kill_instance(*args, **kwargs):
    kill_ret = client.terminate_instances(
       InstanceIds=[
           instance_id
       ]
    )
    print("Instance {0} terminated.".format(instance_id))

signal.signal(signal.SIGTERM, kill_instance)

try:
    subprocess.call(['zsh', '{0}/openvpn.zsh'.format(os.path.dirname(os.path.realpath(__file__))), public_ip, str(args.port)])
except KeyboardInterrupt:
    kill_instance
