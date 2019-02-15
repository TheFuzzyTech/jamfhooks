=====
Jamf Webhook Receiver
=====

This is a utility for to create webhooks in your JSS instance and pointed back
to this server.

Quick start
-----------

1. Add "myblog" to INSTALLED_APPS:
  INSTALLED_APPS = {
    ...
    'jamf_webhook_receiver'
  }

2. Include the myblog URLconf in urls.py:
  url(r'^webhooks/', include('jamf_webhook_receiver.urls'))

3. Run `python manage.py syncdb` to create models.

4. Run the development server and access http://127.0.0.1:8000/admin/ to
    manage.

5. Access http://127.0.0.1:8000/webhooks/ to begin.
