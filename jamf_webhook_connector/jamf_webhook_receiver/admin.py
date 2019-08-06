from django.contrib import admin
from jamf_webhook_receiver.models import JSSServer, SnipeITServer, JSSIntegrations

# Register your models here.
admin.site.register(JSSServer)
admin.site.register(SnipeITServer)
admin.site.register(JSSIntegrations)
