import boto.ec2
import os
import time
from boto.manage.cmdshell import sshclient_from_instance
conn = boto.ec2.connect_to_region("us-east-1",
                                  aws_access_key_id = '<YOUR ID>',
                                  aws_secret_access_key = '<YOUR KEY>')
key_pair = conn.create_key_pair("testgood")
key_pair.save(os.getcwd())
sec_group = conn.create_security_group('testcsc326-group', 'uoft')
sec_group.authorize('icmp', -1, -1, '0.0.0.0/0') #enable ping
sec_group.authorize('tcp', 22, 22, '0.0.0.0/0') #enable ssh
sec_group.authorize('tcp', 80, 80, '0.0.0.0/0') #enable http
reservation = conn.run_instances(
    'ami-9aaa1cf2',
    key_name = 'testgood',
    instance_type = 't2.micro',
    security_groups = ['testcsc326-group'])
time.sleep(10)
inst_id = str(reservation.instances[0].id)
while str(reservation.instances[0].state).lower() != 'running':
    reservation.instances[0].update()
conn.associate_address(instance_id=inst_id, allocation_id='eipalloc-89399aec')
ssh_client = sshclient_from_instance(reservation.instances[0],
                                     key_path='testgood.pem',
                                     user_name='ubuntu')
status, stdout, stderr = ssh_client.exec_command('sudo apt-get install git')
status, stdout, stderr = ssh_client.exec_command('git clone https://github.com/anhuang/Miranda.git')
status, stdout, stderr = ssh_client.exec_command('cd Mirand/frontend')
status, stdout, stderr = ssh_client.exec_command('screen')
status, stdout, stderr = ssh_client.exec_command('sudo python server.py &')
status, stdout, stderr = ssh_client.exec_command('\x03\x04')
status, stdout, stderr = ssh_client.exec_command('logout')
reservation.instances[0].update()
print "IP address is " + str(reservation.instances[0].ip_address)
print "Instance ID is " + str(reservation.instances[0].id)
ssh_client.close()
