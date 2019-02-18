from django.db import models
from django.urls import reverse
# Create your models here.
from django.utils import timezone
import requests

class SnipeServer(models.Model):
        name = models.CharField(max_length=25)
        url = models.URLField(max_length=200, help_text="Your full snipeIT URL")
        ip = models.GenericIPAddressField(default='0.0.0.0')
        username = models.CharField(max_length=255)
        token = models.CharField(max_length=255)

        def __str__(self):
            return self.name

class JSSServer(models.Model):
    JSSSTATUS = (
                ('JSSStartup', "JSSStartup"),
                ('JSSShutdown', "JSSShutdown"),
                )
    name = models.CharField(max_length=25)
    url = models.URLField(max_length=200, help_text="Your full JSS URL")
    status = models.CharField(max_length=11, choices=JSSSTATUS)
    ip = models.GenericIPAddressField(default='0.0.0.0')
    userName = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    '''webhook types'''
    ComputerAdded = models.BooleanField(default=False)
    ComputerCheckIn = models.BooleanField(default=False)
    ComputerInventoryCompleted = models.BooleanField(default=False)
    ComputerPatchPolicyCompleted = models.BooleanField(default=False)
    ComputerPolicyFinished = models.BooleanField(default=False)
    ComputerPushCapabilityChanged = models.BooleanField(default=False)
    DeviceRateLimited = models.BooleanField(default=False)
    JSSShutdown = models.BooleanField(default=False)
    JSSStartup = models.BooleanField(default=False)
    MobileDeviceCheckIn = models.BooleanField(default=False)
    MobileDeviceCommandCompleted = models.BooleanField(default=False)
    MobileDeviceEnrolled = models.BooleanField(default=False)
    MobileDevicePushSent = models.BooleanField(default=False)
    MobileDeviceUnEnrolled = models.BooleanField(default=False)
    PatchSoftwareTitleUpdated = models.BooleanField(default=False)
    PushSent = models.BooleanField(default=False)
    RestAPIOperation = models.BooleanField(default=False)
    SCEPChallenge = models.BooleanField(default=False)
    SmartGroupComputerMembershipChange = models.BooleanField(default=False)
    SmartGroupMobileDeviceMembershipChange = models.BooleanField(default=False)
    #INTEGRATIONS
    SnipeServer = models.ManyToManyField(SnipeServer)


    def get_absolute_url(self):
        return reverse("jss_detail",kwargs={'pk':self.pk})

    def jss_webhook_create(self,url,name,userName,password, webhook_type, webhook_endpoint):
        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/json',
        }
        jss_url = str(url) + "/JSSResource/webhooks/id/0"
        this_server_url = "http://10.140.130.68:8000" #socket.gethostname()
        post_data = """<?xml version="1.0" encoding="UTF-8"?>
        <webhook>
            <name>"""+ name + " " + webhook_type +"""</name>
            <enabled>true</enabled>
            <url>"""+ this_server_url + webhook_endpoint + """</url>
            <content_type>application/json</content_type>
            <event>"""+webhook_type+"""</event>
            <authentication_type>NONE</authentication_type>
            <username/>
            <password/>
            <enable_display_fields_for_group_object>false</enable_display_fields_for_group_object>
            <display_fields>
                <size>0</size>
            </display_fields>
        </webhook>"""
        jss_post = requests.post(jss_url, auth=(userName, password),
                                 headers=headers, verify=False,
                                 data=post_data)
        print(jss_post.text)

    def __str__(self):
        return self.name

class SnipeITServer(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    token = models.CharField(max_length=1000)

    def run(self,serialnumber):
        snipe_url = self.url+"/api/v1/hardware/byserial/"+serialnumber
        snipe_headers = {'Authorization': 'Bearer '+self.token,
                         'Content-Type': 'application/json',
                         'Accept': 'application/json',
                         }
        snipeit_comp_response = requests.get(snipe_url, headers=snipe_headers,)


    def __str__(self):
        return self.name


class JSSIntegrations(models.Model):
    name = models.CharField(max_length=255)
    server = models.ForeignKey('JSSServer', on_delete=models.CASCADE)
    snipe_IT_server = models.ForeignKey('SnipeITServer',on_delete=models.CASCADE)

    def __str__(self):
        return self.name
