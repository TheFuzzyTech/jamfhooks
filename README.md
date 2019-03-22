# jamf_webhook_connector
###### Linux/OSX

`git clone https://github.com/thefuzzyjew/jamf_webhook_connector.git`

run `bash setup.sh` in terminal

visit **127.0.0.1:8000/webhooks**
###### Windows Users






########## SFTP SETUP

Use the .env to setup your ssh user for the container_name

Log in to the container
 `ssh master@container-ip -p 22 # Password is master`
 Add a new SFTP User
`$ sudo mkdir /uploads/inanzzz
$ sudo mkdir /uploads/inanzzz/upload
$ sudo useradd -d /uploads/inanzzz -G sftp inanzzz -s /usr/sbin/nologin
$ echo "inanzzz:inanzzz" | sudo chpasswd
$ sudo chown inanzzz:sftp -R /uploads/inanzzz/upload`

Test the login

`$ sftp inanzzz@container-ip
sftp>`
