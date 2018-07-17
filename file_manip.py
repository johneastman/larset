#!/bin/bash

# Bash script that creates and sets up a laravel project on Windows.
# Written by John Eastman

# Pre-requisites
# 	1. Git			https://git-scm.com/
# 	2. xampp		https://www.apachefriends.org/index.html
# 	3. composer		https://getcomposer.org/

# Parameters:
# 	$1		Project Name
#	$2		Delete project flag (-rm). Optional parameter.
#			https://stackoverflow.com/questions/11576788/delete-text-in-file-using-bash-script-in-linux
#			sed -i '/text_to_delete/d' filename

# Commands:
# $0		  $1	 $2					$3
# ./larset.sh create [project name]
# ./larset.sh delete [project name]
# ./larset.sh rename [old project name] [new project name]

# NOTES:
#	1. Must run Git Bash as administrator to work.
#	2. In this script's current state, two assumptions are made:
# 		a. Assumes that this file is in xampp\htdocs
#		b. Assumes that these files and directories are on the C drive
#	3. Avoid project names with underscores

# Features to Implement:
# 1. Delete projects and remove from vhost and hosts
# 2. Rename a project

# Bash script that creates and sets up a laravel project on Windows.
# Written by John Eastman

function displayInfo() {
	echo "Commands:"
	echo "  $0 create [project name]"
	echo "  $0 delete [project name]"
	echo "  $0 rename [old project name] [new project name]"
}


# Check if a directory/project already exists
function dirExists() {
	if [ ! -d "$1" ]; # $1 in relation to function call, not arguments for file
	then
		echo 1
	else
		echo 0
	fi
}


cwd="$PWD/$2/public"

# Replace '0' with 'u&' to capitalize drive letter
windowsPath=$(echo "$cwd" | sed -e 's/^\///' -e 's/\//\\\\/g' -e 's/^./\0:/')
vhost="<VirtualHost *:80>\n\tDocumentRoot '$windowsPath'\n\tServerName $2.test\n</VirtualHost>"
domain="127.0.0.1 $2.test" # Windows domain

# Set up python script for execution
chmod +x $PWD/file_manip.py


# Check if the user provides a project name.
if [ $# -eq 0 ];
then
	# No arguments will direct user to help output
	displayInfo
	exit 1
elif [ $1 = "create" ]; # Creating a project
then
	# Check if the project already exists before creating
	isdir=`dirExists $2`
	if [ $isdir ];
	then
	
		echo "Creating '$2' ..."
	
		composer create-project --prefer-dist laravel/laravel $2
		
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
		cd ../apache/conf/extra
		echo -e $vhost >> httpd-vhosts.conf
		
		# Add to hosts file:
		# NOTE: hosts at C:\Windows\System32\drivers\etc
		cd /c/Windows/System32/drivers/etc
		echo $domain >> hosts
	else
		echo "Project '$2' already exists"
		exit 1
	fi
elif [ $1 = "delete" ]; # Deleting a project
then
	isdir=`dirExists $2`
	if [ $isdir ];
	then
		echo "Deleting '$2' ..."
		
		# Delete directory
		rm -r $2
		
		pycwd=$PWD # Capture this directory for python script
		
		# Remove virtual host from httpd-vhosts.conf
		cd ../apache/conf/extra
		python $pycwd/file_manip.py $2 $windowsPath  # Planned feature: pass $vhost in here. 
		
		# Remove domain from hosts
		cd /c/Windows/System32/drivers/etc
		sed -i -e "s/$domain.*//" hosts

		exit 0
	else
		echo "Project '$2' does not exist"
		exit 1
	fi
elif [ $1 = "rename" ]; # renaming a project
then
	isdir=`dirExists $2`
	if [ $isdir ];
	then
		echo "Renaming '$2' to '$3' ..."
		
		mv $2 $3 # Rename directory 
		
		cd ../apache/conf/extra
		sed -i -e "s/$2/$3/g" httpd-vhosts.conf
		
		cd /C/Windows/System32/drivers/etc
		sed -i -e "s/$2/$3/g" hosts
		
		exit 0
	else
		echo "Project '$2' does not exist"
		exit 1
	fi
else
	# Under all other circumstances, display commands
	displayInfo
	exit 0
fi
