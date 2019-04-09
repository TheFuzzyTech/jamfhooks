# jamf_webhook_connector
###### Linux/OSX

`git clone https://github.com/thefuzzyjew/jamf_webhook_connector.git`

Edit .env file with your server's FQDN and modify the postgres username and password

run `bash setup.sh` in terminal

visit **127.0.0.1:8000/webhooks**
###### Windows Users






########## SFTP SETUP
The SFTP container is only required if you would like to integrate a service to
upload csv files to the server that django can then interact with.

IE with infinite campus you can have IC upload a csv of newly created students.

You can then have Django read that CSV and create new Active Directory Users

based off of the csv.

Use the .env to setup your ssh user for the container_name

Log in to the container
 `ssh master@container-ip -p 22 # Password is master`
 Add a new SFTP User
`$ sudo mkdir /uploads/youruser
$ sudo mkdir /uploads/youruser/upload
$ sudo useradd -d /uploads/youruser -G sftp youruser -s /usr/sbin/nologin
$ echo "youruser:youruser" | sudo chpasswd
$ sudo chown youruser:sftp -R /uploads/youruser/upload`

Test the login

`$ sftp inanzzz@container-ip
sftp>`
