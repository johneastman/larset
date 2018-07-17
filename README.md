# larset
A bash script that creates and sets up a laravel project on Windows. I wrote this script while I was working on a Udemy course on Laravel. 

### Pre-requisites
  1. [Git](https://git-scm.com/)
  2. [xampp](https://www.apachefriends.org/index.html)
  3. [composer](https://getcomposer.org/)

### Commands
| Operation                          | Command                                                  |
|:-----------------------------------|:---------------------------------------------------------|
| Create a new laravel project       | ./larset.sh create [project name]                        |
| Delete an existing laravel project | ./larset.sh delete [project name]                        |
| Rename an existing laravel project | ./larset.sh rename [old project name] [new project name] |

### Notes
  1. Must run Git Bash as administrator.
  2. This script must be placed in xampp\htdocs directory.
  3. Avoid project names with underscores in them.
