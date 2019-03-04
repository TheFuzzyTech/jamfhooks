#macOS and Linux setup script
docker-compose build
docker-compose up --no-start
docker-compose run web python jamf_webhook_connector/manage.py createsuperuser
docker start jamf_webhook_receiver_db_1
docker start jamf_webhook_receiver_web_1
