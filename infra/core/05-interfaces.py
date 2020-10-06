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
#print(t.keys())

#for key in t.keys():
#    print(key)
#    print(t[key])

nodes=t["nodes"]
interfaces=t["interfaces"]
links=t["links"]

for node in nodes:
    id=node["id"]
    type=node["data"]["node_definition"]
    name=node["data"]["label"]
    print("Id {} type {} label {}".format(id,type,name))
    
    interface_config=[]
    for interface in interfaces:
        if interface["node"]==id:
           ifname=interface["data"]["label"]
           ifid=interface["id"]
           #print("   Interface {} id {}".format(ifname,ifid))

           for link in links:
               ifid_a=link["interface_a"]
               node_a_id,ifname_a=[ [x["node"],x["data"]["label"]] for x in interfaces if x["id"]==ifid_a][0]
               node_a_name=[ x["data"]["label"] for x in nodes if x["id"]==node_a_id ][0]
               ifid_b=link["interface_b"]
               node_b_id,ifname_b=[ [x["node"],x["data"]["label"]] for x in interfaces if x["id"]==ifid_b][0]
               node_b_name=[ x["data"]["label"] for x in nodes if x["id"]==node_b_id ][0]

               if ifid_a==ifid or ifid_b==ifid:
       
                  if ifid_b==ifid:
                     ifid_b=ifid_a
                     ifid_a=ifid
                  
                  node_a_id,ifname_a=[ [x["node"],x["data"]["label"]] for x in interfaces if x["id"]==ifid_a][0]
                  node_a_name=[ x["data"]["label"] for x in nodes if x["id"]==node_a_id ][0]

                  node_b_id,ifname_b=[ [x["node"],x["data"]["label"]] for x in interfaces if x["id"]==ifid_b][0]
                  node_b_name=[ x["data"]["label"] for x in nodes if x["id"]==node_b_id ][0]
                
                  print("   Link between {} on {} and {} on {}".format(ifname_a,node_a_name,ifname_b,node_b_name))

                  if node_a_name[0]==node_b_name[0]=="R":

                    interface_config.append("     interface {}".format(ifname_a))
                    interface_config.append("        description from {} to {}".format(node_a_name,node_b_name))
                    interface_config.append("        no shutdown")
               
                    mine=int(name[1:])
                    first=int(node_a_name[1:]) if int(node_a_name[1:])>int(node_b_name[1:]) else int(node_b_name[1:])
                    second=int(node_b_name[1:]) if int(node_a_name[1:])>int(node_b_name[1:]) else int(node_a_name[1:])

                    if type=="iosxrv":
                        interface_config.append("        ipv4 address 10.{}.{}.{} 255.255.255.0".format(first,second,mine))
                    else:
                        interface_config.append("        ip  address 10.{}.{}.{} 255.255.255.0".format(first,second,mine))
    
    if interface_config:
        node_ip="192.168.255."+name[1:]
        print("   {} {}".format(name,node_ip))

        rtr_session = ConnectHandler(device_type='cisco_ios',host=node_ip,username='cisco',password='cisco')
        
        if type=="iosxrv":
            interface_config+=["commit"]
        interface_config+=["end"]

        output=rtr_session.send_config_set(interface_config)
        #print(output)
        if type=="iosxe":
            rtr_session.send_command("wr mem")

