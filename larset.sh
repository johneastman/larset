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


# ----------------------------------------------------
# Add project to virtual host file: httpd-vhosts.conf 
# NOTE: httpd-vhosts.conf at xampp\apache\conf\extra  
# ----------------------------------------------------

# Replaces the current working directory (in POSIX form) to Windows Path form
# Example:
#    POSIX:     /D/Coding/Projects/Shell
#    Windows:   D:/Coding/Projects/Shell/hello/public
# Source: https://stackoverflow.com/questions/13701218/windows-path-to-posix-path-conversion-in-bash
# NOTE: $PWD will be 'xampp\apache\conf\extra'
cwd="$PWD/$1/public"
windowsPath=`echo "$cwd" | sed -e 's/^\///' -e 's/^./\0:/'`
vhost="\n\n<VirtualHost *:80>\n\tDocumentRoot '$windowsPath'\n\tServerName $1.test\n</VirtualHost>"
cd ../apache/conf/extra
echo -e $vhost >> httpd-vhosts.conf


# Add to hosts file:
# NOTE: hosts at C:\Windows\System32\drivers\etc
cd /C/Windows/System32/drivers/etc
echo "127.0.0.1 $1.test" >> hosts

exit 0
