#macOS and Linux setup script
docker-compose build --no-cache
docker-compose up --force-recreate
#sleep to let migrations finish
echo "Waiting for Migrations..."
sleep 10
# Create a super user
docker exec -it $(docker ps -aqf "name=jamfhooks_web") python jamf_webhook_connector/manage.py createsuperuser
echo "visit 127.0.0.1:8000/admin to log in"
echo "visit 127.0.0.1:8000/webhooks after logging in to begin"
#docker-compose run web python jamf_webhook_connector/manage.py createsuperuser
#docker start jamfhooks_db
#docker start jamfhooks_web
