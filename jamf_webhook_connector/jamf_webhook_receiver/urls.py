"""jamf_webhook_connector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from jamf_webhook_receiver import views
from django.conf.urls import url


urlpatterns = [
    path('', views.AboutView.as_view(),name="index"),
    url(r'^jss/$',views.JSSListView.as_view(),name='jss_list'),
    path('jssstatus', views.jssstatus),
    path('ComputerCheckIn', views.computer_checkin),
    url(r'^about/$', views.AboutView.as_view(),name='about'),
    url(r'^jss/(?P<pk>\d+$)',views.JSSDetailView.as_view(),name='jss_detail'),
    url(r'^jss/new/$', views.CreateJSSView.as_view(), name='jss_new'),
    url(r'^jss/(?P<pk>\d+)/edit/$',views.JSSUpdateView.as_view(), name='jss_edit'),
    url(r'^jss/(?P<pk>\d+)/remove/$',views.JSSDeleteView.as_view(),name='jss_remove'),
    url(r'^jss/(?P<pk>\d+)/integrations/$',views.IntegrationListView.as_view(),name='integration_list'),
    url(r'^jss/(?P<pk>\d+)/integrations/new/$',views.CreateIntegrationView.as_view(),name='integration_new'),
    url(r'^jss/(?P<pk_1>\d+)/integrations/(?P<pk>\d+)/edit/$',views.IntegrationUpdateView.as_view(),name='integration_edit'),
    url(r'^jss/(?P<pk_1>\d+)/integrations/(?P<pk>\d+)/remove/$',views.IntegrationDeleteView.as_view(),name='integration_remove')
]
