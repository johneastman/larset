#!/bin/bash

# Bash script that creates and sets up a laravel project on Windows.
# Written by John Eastman

# Check if the user provides a project name.
if [ $# -eq 0 ];
then
	echo "No arguments supplied. Must provide project name"
	echo "Syntax: $0 [project name]"  # $0 is the name of this file
	exit 1
fi


# Create the project if it doesn't exist
if [ ! -d "$1" ];
then
	composer create-project --prefer-dist laravel/laravel $1 5.2.29
else
	echo "Project '$1' already exists"
	exit 1
fi


# Add project to virtual host file: httpd-vhosts.conf 
# NOTE: httpd-vhosts.conf at xampp\apache\conf\extra
vhost="\n\n<VirtualHost *:80>\n	DocumentRoot 'C:/Coding/xampp/htdocs/$1/public'\n	ServerName $1.test\n</VirtualHost>"
cd ../apache/conf/extra
echo -e $vhost >> httpd-vhosts.conf


# Add to hosts file:
# NOTE: hosts at C:\Windows\System32\drivers\etc
cd /C/Windows/System32/drivers/etc
echo "127.0.0.1 $1.test" >> hosts

exit 0
