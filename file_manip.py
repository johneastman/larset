#!/usr/bin/env python

import sys
import os

# Laravel project name
project_name = sys.argv[1]
path = sys.argv[2]

to_remove = "<VirtualHost *:80>\n    DocumentRoot '{}'\n    ServerName {}.test\n</VirtualHost>".format(path, project_name)


os.chdir("..")
os.chdir(os.getcwd() + "\\extra")

with open("httpd-vhosts.conf", "r") as input:
	lines = input.read()
	
	with open("httpd-vhosts.conf", "w") as output:
		
		for line in lines.split("\n\n"):
			temp_line = line
			if temp_line.strip("\n").strip("\t") != to_remove.strip("\n").strip("\t"):
				output.write(line + "\n\n")

			