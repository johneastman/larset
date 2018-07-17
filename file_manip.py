#!/usr/bin/env python

import sys
import os

# Laravel project name
project_name = sys.argv[1]
path = sys.argv[2]

to_remove = "<VirtualHost *:80>\n\tDocumentRoot '{}'\n\tServerName {}.test\n</VirtualHost>".format(path, project_name)


os.chdir("..")
os.chdir(os.getcwd() + "\\extra")

with open("httpd-vhosts.conf", "r") as input:
	lines = input.readlines()
	
	vhosts = []
	vhost = ""
	block = False  # Text within vhost tag
	for line in lines:
		
		
		if "<VirtualHost *:80>" in line:
			block = True
			
		if "</VirtualHost>" in line:
			block = False
			vhost += line
			vhosts.append(vhost)
			vhost = ""
		
		if block:
			vhost += line
	
	with open("httpd-vhosts.conf", "w") as output:
		
		for _vhost in vhosts:
			temp_vhost = "".join(_vhost.split())
			to_remove = "".join(to_remove.split()).replace("\\\\", "\\")
			
			if temp_vhost != to_remove:
				output.write(_vhost + "\n\n")
			
