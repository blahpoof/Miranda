import boto.ec2
import os
import time
conn = boto.ec2.connect_to_region("us-east-1",
                                  aws_access_key_id = '<YOUR ID>',
                                  aws_secret_access_key = '<YOUR KEY>')
insts = conn.terminate_instances(instance_ids=['<INSTANCE_ID>'])
while str(insts.state).lower() != 'terminated':
    insts.update()
print "Termination Successful"
