from django.db import models
from django.urls import reverse
# Create your models here.
from django.utils import timezone
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
            <authentication_type>none</authentication_type>
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
    token = models.CharField(max_length=4000)

    def run(self,serialnumber,devicename,jss_url,jss_user,jss_password):
        snipe_url = self.url+"/api/v1/hardware/byserial/{}".format(serialnumber)
        snipe_headers = {'Authorization': 'Bearer '+self.token,
                         'Content-Type': 'application/json',
                         'Accept': 'application/json',
                         }
        snipeit_comp_response = requests.get(snipe_url, headers=snipe_headers,)
        snipeit_comp_data = snipeit_comp_response.json()
        if snipeit_comp_response.status_code != 200:
            return("NON 200 STATUS")
        else:
            '''If Device Not In Snipe'''
            if snipeit_comp_data['total'] == 0:
                #return("ASSET NOT IN SNIPE")
                '''ADD LOGIC HERE TO ADD THE DEVICE TO SNIPE'''
                '''Get More Info about the Computer'''
                jss_headers = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                }
                try:
                    jss_asset_response = requests.get("{}/JSSResource/computers/serialnumber/{}".format(jss_url,serialnumber), auth=(jss_user, jss_password), headers=jss_headers, verify=False)

                    if jss_asset_response.status_code != 200:
                        '''IF JSS RETURNS NON 200STATUS'''
                        response_code = "Response code: "+str(jss_asset_response.status_code)
                        jss_asset_result = response_code
                        return(response_code)
                    else:
                        jss_asset_result =  json.loads(jss_asset_response.text)
                        #print(jss_asset_response.text)
                        jss_computer_name = (jss_asset_result['computer']['general']['name'])
                        jss_asset_tag = (jss_asset_result['computer']['general']['asset_tag'])
                        jss_user_name = (jss_asset_result['computer']['location']['username'])
                        jss_real_name = (jss_asset_result['computer']['location']['real_name'])
                        # jss_email = (jss_asset_result['computer']['location']['email_address'])
                        # jss_phone = (jss_asset_result['computer']['location']['phone'])
                        # jss_phone_number = (jss_asset_result['computer']['location']['phone_number'])
                        # jss_department = (jss_asset_result['computer']['location']['department'])
                        # jss_building = (jss_asset_result['computer']['location']['building'])
                        # jss_purchase_date = (jss_asset_result['computer']['purchasing']['po_date'])
                        jss_model = (jss_asset_result['computer']['hardware']['model'])
                        if jss_asset_tag == '':
                            return("No asset Tag in Jamf, Cannot Create in Snipe")
                        else:
                            '''This is Where the device gets created in snipe if possible'''
                            '''GET ALL MODELS FROM SNIPE TO TRY TO MATCH MODELS'''
                            snipe_model_url = self.url+"/api/v1/models"
                            model_params ={"search": jss_model}
                            snipeit_model_response = requests.get(snipe_model_url, headers=snipe_headers,params=model_params)
                            snipeit_model_data = snipeit_model_response.json()
                            if snipeit_model_response.status_code != 200:
                                return("NON 200 STATUS")
                            else:
                                #return(snipeit_model_data['rows'][0])
                                if snipeit_model_data['rows'][0]['name'] != jss_model:
                                    return("Models do not match")
                                else:
                                    snipe_model_id = snipeit_model_data['rows'][0]['id']
                                    snipe_create_asset = {}
                                    snipe_create_asset['asset_tag'] = jss_asset_tag
                                    snipe_create_asset['status_id'] = 1 #1=Ready to Deploy. This will be the default unil device is checked out
                                    snipe_create_asset['model_id'] = snipe_model_id
                                    snipe_create_asset['name'] = jss_computer_name
                                    snipe_create_asset['serial'] = serialnumber
                                    #return("Device",jss_computer_name, jss_asset_tag, jss_model, "Not in Snipe")
                                    snipe_create_asset_url = self.url+"/api/v1/hardware/"
                                    snipeit_create_asset_response = requests.post(snipe_create_asset_url, headers=snipe_headers,json=snipe_create_asset)
                                    snipeit_create_asset_data = snipeit_create_asset_response.json()
                                    if snipeit_create_asset_response.status_code != 200:
                                        return("NON 200 STATUS")
                                    else:
                                        create_asset_status = snipeit_create_asset_data['status']
                                        if create_asset_status == 'error':
                                            create_asset_message = snipeit_create_asset_data['messages']
                                            return(jss_asset_tag,create_asset_status,create_asset_message)
                                        else:
                                            return(jss_asset_tag, create_asset_status)
                except ConnectionResetError:
                    return("Connection Reset")



            else:
                '''IF Device is in Snipe'''
                jss_headers = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                }
                try:
                    jss_asset_response = requests.get("{}/JSSResource/computers/serialnumber/{}".format(jss_url,serialnumber), auth=(jss_user, jss_password), headers=jss_headers, verify=False)

                    if jss_asset_response.status_code != 200:
                        '''IF JSS RETURNS NON 200STATUS'''
                        response_code = "Response code: "+str(jss_asset_response.status_code)
                        jss_asset_result = response_code
                        return(response_code)
                    else:
                        jss_asset_result =  json.loads(jss_asset_response.text)
                        #print(jss_asset_response.text)
                        jss_computer_name = (jss_asset_result['computer']['general']['name'])
                        jss_asset_tag = (jss_asset_result['computer']['general']['asset_tag'])
                        jss_user_name = (jss_asset_result['computer']['location']['username'])
                        jss_real_name = (jss_asset_result['computer']['location']['real_name'])
                        # jss_email = (jss_asset_result['computer']['location']['email_address'])
                        # jss_phone = (jss_asset_result['computer']['location']['phone'])
                        # jss_phone_number = (jss_asset_result['computer']['location']['phone_number'])
                        # jss_department = (jss_asset_result['computer']['location']['department'])
                        # jss_building = (jss_asset_result['computer']['location']['building'])
                        # jss_purchase_date = (jss_asset_result['computer']['purchasing']['po_date'])
                        asset_tag = (snipeit_comp_data['rows'][0]['asset_tag'])
                        status = (snipeit_comp_data['rows'][0]['status_label']['status_meta'])
                        computer_name = (snipeit_comp_data['rows'][0]['name'])
                        snipe_comp_id = (snipeit_comp_data['rows'][0]['id'])
                        '''ADD LOGIC HERE TO DETERMINE IF DEVICE INFO IS CORRECT'''
                        snipe_patch_payload={}
                        if computer_name == jss_computer_name:
                            return("names up to date")
                            if asset_tag == jss_asset_tag:
                                if jss_user_name == "Snipe Checked Out to":
                                    return("Device up to date")
                                else:
                                    '''Add logic here to check out device to snipe user'''
                            else:
                                '''Add Logic here for if asset tags to not match'''
                        else:
                            '''Logic for if the names do not match'''
                            snipe_patch_payload['name'] = jss_computer_name
                            snipe_patch_payload['serial']= serialnumber
                            snipe_name_url = self.url+"/api/v1/hardware/{}".format(snipe_comp_id)
                            snipe_headers = {'Authorization': 'Bearer {}'.format(self.token),
                                             'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             }
                            snipeit_name_response = requests.put(snipe_name_url,json=snipe_patch_payload, headers=snipe_headers,)
                            snipeit_name_data = snipeit_name_response.json()
                            if snipeit_name_response.status_code != 200:
                                return(snipeit_name_data.status_code)
                            else:
                                return("Name Updated", asset_tag,jss_computer_name,)
                except ConnectionResetError:
                        return("Connection Reset")



    def __str__(self):
        return self.name


class JSSIntegrations(models.Model):
    name = models.CharField(max_length=255)
    server = models.ForeignKey('JSSServer', on_delete=models.CASCADE)
    snipe_IT_server = models.ForeignKey('SnipeITServer',on_delete=models.CASCADE)


    def __str__(self):
        return self.name
