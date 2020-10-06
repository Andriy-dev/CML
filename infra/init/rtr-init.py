#!/usr/bin/python3

# inventory
# n1      R2         TCP/9002

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

token=resp.json()

resp = requests.get('https://10.0.1.70/api/v0/labs/'+lab_id+'/topology?exclude_configurations=false',headers={'Authorization': 'Bearer {}'.format(token)},verify=False)

t=resp.json()

resp = requests.get('https://10.0.1.70/api/v0/labs/'+lab_id+'/topology?exclude_configurations=false',headers={'Authorization': 'Bearer {}'.format(token)},verify=False)

t=resp.json()

nodes=t["nodes"]

for node in nodes:
    node_id=node["id"]
    id=str(int(node["id"][1:])+1)
    type=node["data"]["node_definition"]
    label=node["data"]["label"]
    name="R"+id
    print("Id {} type {} label {} name {}".format(id,type,label,name))
    if type=="csr1000v":
        with open("xe-template.txt") as csr:
            config="".join([line for line in csr])
            config=config.replace("{router}",name)
            config=config.replace("{ip}","192.168.255."+id)
            #print("==="*20)
            #print(config)
            resp = requests.put('https://10.0.1.70/api/v0/labs/'+lab_id+'/nodes/'+node_id+'/config',headers={'Authorization': 'Bearer {}'.format(token) ,'Content-Type': 'text/plain' },data=config.encode('utf-8'),verify=False)

            t=resp.json()
            print(t)



            


