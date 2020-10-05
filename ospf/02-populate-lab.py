from netmiko import ConnectHandler
import requests

task={ "username":"admin", "password":"sysadmin" }
base='https://10.0.1.70/api/v0'
lab='d6a085'
number_of_nodes=10

resp = requests.post(base+ "/authenticate",json=task,verify=False)

if resp.status_code != 200:
    raise Exception('POST /api/v0/authenticate {}'.format(resp.status_code))

token=resp.json()

resp = requests.post(base + '/labs/' + lab ,headers={'Authorization': 'Bearer {}'.format(token),'node_definition':'CSR1000v 16.11.01b'},verify=False)

t=resp.json()

print(t)


