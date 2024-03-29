#macOS and Linux setup script
docker-compose build --no-cache
docker-compose up -d --force-recreate
#sleep to let migrations finish
echo "Waiting for Migrations..."
sleep 10
# Create a super user
if [ $TESTING = true ]; then
  echo "Testing, skip user creation"
else
  docker exec -it $(docker ps -aqf "name=jamfhooks_web") python manage.py createsuperuser
fi
echo "visit 127.0.0.1/admin to log in"
echo "visit 127.0.0.1/webhooks after logging in to begin"
#docker-compose run web python jamf_webhook_connector/manage.py createsuperuser
#docker start jamfhooks_db
#docker start jamfhooks_web
