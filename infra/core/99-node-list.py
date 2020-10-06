#!/usr/bin/python3

import requests
import sys
from netmiko import ConnectHandler
import os

if os.environ.get('LAB_ID') is None:
        print('Set LAB_ID environment variable')
        sys.exit()

lab_id=os.environ.get('LAB_ID')

task={ "username":"admin", "password":"sysadmin" }

resp = requests.post('https://10.0.1.70/api/v0/authenticate',json=task,verify=False)

if resp.status_code != 200:
        raise Exception('POST /tasks/ {}'.format(resp.status_code))

#print("{}".format(resp.json()))
token=resp.json()
#print("Got token {}".format(token))

resp = requests.get('https://10.0.1.70/api/v0/labs/'+lab_id+'/topology?exclude_configurations=false',headers={'Authorization': 'Bearer {}'.format(token)},verify=False)

t=resp.json()

nodes=t["nodes"]

for node in nodes:
    id=node["id"]
    node_type=node["data"]["node_definition"]
    name=node["data"]["label"]
    node_ip="192.168.255."+name[1:]
    print("{: >10} {: >10} {: >10} {: >10}".format(id,node_type,name,node_ip))

