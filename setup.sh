#macOS and Linux setup script
docker-compose build
docker-compose up -d
#sleep to let migrations finish
echo "Waiting for Migrations..."
sleep 10
# Create a super user
docker exec -it $(docker ps -aqf "name=jamfhooks_web") python jamf_webhook_connector/manage.py createsuperuser

#docker-compose run web python jamf_webhook_connector/manage.py createsuperuser
#docker start jamfhooks_db
#docker start jamfhooks_web
