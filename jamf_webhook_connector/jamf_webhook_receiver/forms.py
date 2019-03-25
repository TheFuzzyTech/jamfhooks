from django import forms
from jamf_webhook_receiver.models import JSSServer, JSSIntegrations

class JSSServerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = JSSServer
        fields = ('name','url','userName','password','ComputerAdded',
                    'ComputerCheckIn',
                    'ComputerInventoryCompleted',
                    'ComputerPatchPolicyCompleted',
                    'ComputerPolicyFinished',
                    'ComputerPushCapabilityChanged',
                    'DeviceRateLimited',
                    'JSSShutdown',
                    'JSSStartup',
                    'MobileDeviceCheckIn',
                    'MobileDeviceCommandCompleted',
                    'MobileDeviceEnrolled',
                    'MobileDevicePushSent',
                    'MobileDeviceUnEnrolled',
                    'PatchSoftwareTitleUpdated',
                    'PushSent',
                    'RestAPIOperation',
                    'SCEPChallenge',
                    'SmartGroupComputerMembershipChange',
                    'SmartGroupMobileDeviceMembershipChange',)
        widgets = {
            'title':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class JSSIntegrationsForm(forms.ModelForm):
    class Meta:
        model = JSSIntegrations
        fields = ('name','server','snipe_IT_server')
