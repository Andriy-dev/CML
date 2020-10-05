#!/usr/bin/python3

import sys

with open("inventory.txt","r") as inventory:
	for line in inventory.readlines():
		[rtr,ip,type]=line[:-1].split()
		header='#'+'='*20+rtr+'='*20
		print(header)
		
		if type=="XR":	
			template="xr-template.txt"
		if type=="XE":
			template="xe-template.txt"
		with open(template,"r") as template:
                        for line in template.readlines():
                                line=line[:-1]
                                line=line.replace("{router}",rtr)
                                line=line.replace("{ip}",ip)
                                print(line)
