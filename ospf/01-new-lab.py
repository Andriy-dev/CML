from netmiko import ConnectHandler
import requests

task={ "username":"admin", "password":"sysadmin" }
base='https://10.0.1.70/api/v0'

resp = requests.post(base+ "/authenticate",json=task,verify=False)

if resp.status_code != 200:
    raise Exception('POST /api/v0/authenticate {}'.format(resp.status_code))

token=resp.json()

resp = requests.post(base + '/labs?title=OSPF',headers={'Authorization': 'Bearer {}'.format(token)},verify=False)

t=resp.json()

print(t)

resp = requests.get( base + '/labs',headers={'Authorization': 'Bearer {}'.format(token)},verify=False)

t=resp.json()

print(t)

