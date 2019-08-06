# jamfhooks
[![Build Status](https://travis-ci.org/thefuzzyjew/jamfhooks.svg?branch=master)](https://travis-ci.org/thefuzzyjew/jamfhooks)
PR's Welcome.

This is a work in progress. I currently have one integration working and am working on ways to clean up the code for future integrations. Right now you can sync Jamf assets into SnipeIT for automatic asset creation and name updating. The idea is that mo

This is my first 'major' project so any feedback is appreciated.

Needed:
- I could use some help with the front end design. Right now everything is functional, but a pretty UI would be nice.
- A better way to determine which modules should be run.




###### Linux/OSX

Modify .env file to fit your needs.

`git clone https://github.com/thefuzzyjew/jamf_webhook_connector.git`

run `bash setup.sh` in terminal

visit **127.0.0.1:8000/webhooks**
###### Windows Users
