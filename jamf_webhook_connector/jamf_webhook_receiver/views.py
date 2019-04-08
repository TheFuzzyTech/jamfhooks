from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import requests
from urllib.parse import urlparse
from jamf_webhook_receiver.models import JSSServer, JSSIntegrations
from jamf_webhook_receiver.forms import JSSServerForm, JSSIntegrationsForm
import socket
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,
                                UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import os
# Create your views here.
'''NEED A WAY TO DYNAMICALLY ADD IP'S HERE'''
allowed_ip = ['10.140.1.161', '173.215.118.194', '10.140.130.68']

class AboutView(TemplateView):
    template_name = 'index.html'


# INTEGRATION VIEWS


class IntegrationListView(ListView):
    model = JSSIntegrations

class IntegrationDetailView(DetailView):
    model = JSSIntegrations


class IntegrationUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'jamf_webhook_receiver/integration_detail.html'
    form_class = JSSIntegrationsForm
    model = JSSIntegrations

class IntegrationDeleteView(LoginRequiredMixin, DeleteView):
    model = JSSIntegrations
    success_url = reverse_lazy('integrations_list')

class CreateIntegrationView(LoginRequiredMixin, CreateView):
    login_url = '/admin/'
    redirect_field_name = 'jamf_webhook_receiver/jssserver_detail.html'
    form_class = JSSIntegrationsForm
    model = JSSIntegrations

# JSS VIEWS

class JSSListView(ListView):
    model = JSSServer


class JSSDetailView(DetailView):
    model = JSSServer

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the integrations
        context['integrations'] = JSSIntegrations.objects.all()
        context['this_pk'] = JSSServer.objects.get(pk=self.kwargs.get('pk'))
        return context


class JSSUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'jamf_webhook_receiver/jss_detail.html'
    form_class = JSSServerForm
    model = JSSServer

class JSSDeleteView(LoginRequiredMixin, DeleteView):
    model = JSSServer
    success_url = reverse_lazy('jss_list')

class CreateJSSView(LoginRequiredMixin, CreateView):
    login_url = '/admin/'
    redirect_field_name = 'jamf_webhook_receiver/jss_detail.html'
    form_class = JSSServerForm
    model = JSSServer

    def form_valid(self, form):
        '''This is an example of how to modify data in a class based view'''
        '''I NEED A BETTER WAY TO DO THIS IP GET'''
        url = urlparse(form.instance.url)
        form.instance.ip = socket.gethostbyname(url.netloc.split(':')[0])
        '''CREATE JSS FUNCTION'''
        def jss_webhook_create(username, password,url, name, webhook_type, webhook_endpoint):
            headers = {
                'Content-Type': 'application/xml',
                'Accept': 'application/json',
            }
            jss_url = str(url) + "/JSSResource/webhooks/id/0"
            this_server_url = "http://{ip}".format(os.getenv(ip='FQDN')) #socket.gethostname()
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
            jss_post = requests.post(jss_url, auth=(username, password),
                                     headers=headers, verify=False,
                                     data=post_data)
            print(jss_post.text)
        '''Create Webhooks'''
        webhook_types ={"ComputerAdded":form.instance.ComputerAdded,
                        "ComputerCheckIn":form.instance.ComputerCheckIn,
                        "ComputerInventoryCompleted":form.instance.ComputerInventoryCompleted,
                        "ComputerPatchPolicyCompleted":form.instance.ComputerPatchPolicyCompleted,
                        "ComputerPolicyFinished":form.instance.ComputerPolicyFinished,
                        "ComputerPushCapabilityChanged":form.instance.ComputerPushCapabilityChanged,
                        "DeviceRateLimited":form.instance.DeviceRateLimited,
                        "JSSShutdown":form.instance.JSSShutdown,
                        "JSSStartup":form.instance.JSSStartup,
                        "MobileDeviceCheckIn":form.instance.MobileDeviceCheckIn,
                        "MobileDeviceCommandCompleted":form.instance.MobileDeviceCommandCompleted,
                        "MobileDeviceEnrolled":form.instance.MobileDeviceEnrolled,
                        "MobileDevicePushSent":form.instance.MobileDevicePushSent,
                        "MobileDeviceUnEnrolled":form.instance.MobileDeviceUnEnrolled,
                        "PatchSoftwareTitleUpdated":form.instance.PatchSoftwareTitleUpdated,
                        "PushSent":form.instance.PushSent,
                        "RestAPIOperation":form.instance.RestAPIOperation,
                        "SCEPChallenge":form.instance.SCEPChallenge,
                        "SmartGroupComputerMembershipChange":form.instance.SmartGroupComputerMembershipChange,
                        "SmartGroupMobileDeviceMembershipChange":form.instance.SmartGroupMobileDeviceMembershipChange,}
        for k,v in webhook_types.items():
            if v:
                form.instance.jss_webhook_create(url=form.instance.url,
                                                name=form.instance.name,
                                                password=form.instance.password,
                                                userName=form.instance.userName,
                                                webhook_type=k,
                                                webhook_endpoint="/webhooks/" + k,)
        return super(CreateJSSView, self).form_valid(form)



@require_POST
@csrf_exempt
def jssstatus(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        request_data = json.loads(request.body.decode("utf-8"))
        jss_status_model = JSSStatus.objects.get()
        #print(ip)
        if ip in allowed_ip:
            jss_status = request_data['webhook']['webhookEvent']
            if jss_status == 'JSSShutdown':
                jss_status_model.status = jss_status
                jss_status_model.save()
                print('JSS SHUTDOWN')
            elif jss_status == 'JSSStartup':
                jss_status_model.Status = jss_status
                jss_status_model.save()
                print('JSS ALIVE')
            else:
                return HttpResponse('ERROR')

            return HttpResponse('Pong')
        else:
            return HttpResponseForbidden('Permissions denied')

        '''STATUS JSON LOOKS LIKE:
        {
        "event": {
            "hostAddress": "172.31.16.70",
            "institution": "Company Name",
            "isClusterMaster": false,
            "jssUrl": "https://company.jamfcloud.com/",
            "webApplicationPath": "/usr/local/jss/tomcat/webapps/ROOT"
        },
        "webhook": {
            "id": 7,
            "name": "Webhook Documentation",
            "webhookEvent": "JSSShutdown"
        }
    }
    '''
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
'''TO DO:   Add authentication
            Add Integration Interaction
            '''
@require_POST
@csrf_exempt
def computer_checkin(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        if ip in allowed_ip:
            request_data = json.loads(request.body.decode("utf-8"))
            serial_number = request_data['event']['serialNumber']
            device_name = request_data['event']['deviceName']
            #print(request_data)
            integrations = JSSIntegrations.objects.filter().select_related()
            jss_server = JSSServer.objects.filter(ip=ip)[0]
            jss_url = jss_server.url
            jss_user = jss_server.userName
            jss_password = jss_server.password
            for integration in integrations:
                print(integration.snipe_IT_server.run(serial_number,device_name,jss_url,jss_user,jss_password))

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=404)
        # if ip in allowed_ip:
        #     #print(request_data['webhook']['webhookEvent'])
        #     return HttpResponse('Pong')
        # else
        #     return HttpResponseForbidden('Permission denied')
