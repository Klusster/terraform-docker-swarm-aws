#!/usr/bin/env python
import boto3
from botocore.exceptions import NoCredentialsError
import os
import subprocess
import time

# Load system daemons
subprocess.check_call(["systemctl", "daemon-reload"])
subprocess.check_call(["systemctl", "enable", "docker.service"])
subprocess.check_call(["systemctl", "start", "docker.service"])

# Set values loaded by the tempalte
s3_bucket = '${s3_bucket}'
region_name = '${region_name}'
instance_index = int('${instance_index}')
vpc_name = '${vpc_name}'

# Set the host name
subprocess.check_call(["hostnamectl", "set-hostname",
                       "worker%d-%s" % (instance_index, vpc_name)])

s3 = boto3.resource('s3', region_name=region_name)
try:
    bucket = s3.Bucket(s3_bucket)
    bucket.objects.all()
except NoCredentialsError as e:
    time.sleep(5)
worker_token_object = s3.Object(s3_bucket, 'worker_token')
manager0_ip_object = s3.Object(s3_bucket, 'ip0')
worker_token_object.wait_until_exists()
manager0_ip_object.wait_until_exists()

worker_token = worker_token_object.get()['Body'].read()
manager0_ip = manager0_ip_object.get()['Body'].read()
subprocess.check_call(
    ["docker", "swarm", "join", "--token", worker_token, manager0_ip])

subprocess.check_output(["mkswap", "/dev/xvdf"])
f = open("/etc/fstab", "a")
f.write("/dev/xvdf none swap defaults 0 0\n")
f.close()
subprocess.check_output(["swapon", "-a"])
