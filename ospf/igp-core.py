from netmiko import ConnectHandler
import requests

lab_id="4629f2"

task={ "username":"admin", "password":"sysadmin" }

resp = requests.post("https://10.0.1.70/api/v0/authenticate",json=task,verify=False)

if resp.status_code != 200:
    raise Exception('POST /api/v0/authenticate {}'.format(resp.status_code))

token=resp.json()

resp = requests.get('https://10.0.1.70/api/v0/labs/697be9/topology?exclude_configurations=false',headers={'Authorization': 'Bearer {}'.format(token)},verify=False)

t=resp.json()

nodes=t["nodes"]
for node in nodes:
    id=node["id"]
    node_type=node["data"]["node_definition"]
    name=node["data"]["label"]
    if node_type=="iosxrv":
        print("Id {} type {} label {}".format(id,node_type,name))
        node_ip="192.168.255."+name[1:]
        rtr_session = ConnectHandler(device_type='cisco_ios',host=node_ip,username='cisco',password='cisco')
        lines=rtr_session.send_command("show ip interface brief")
        config=["interface Loopback0","  ipv4 address 192.168.100.{}/32".format(name[1:]),"router ospf 1","  address-family ipv4 unicast","  area 0","    interface Loopback0"]
        for line in lines.split("\n"):
            #print(line)
            if "GigabitEthernet" in line and "unassigned" not in line:
                ifname=line.split()[0]
                config.append("    interface {}".format(ifname))
                config.append("      network point-to-point")
                config.append("      prefix-suppression")
        config.append("commit")
        output=rtr_session.send_config_set(config)

                
