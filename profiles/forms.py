from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from profiles.models import *
from django.conf import settings
from django.utils.translation import ugettext as _
import urllib
import urllib2
import json


class MyRegistrationForm(UserCreationForm):

    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
    def clean_email(self):
        return self.cleaned_data.get('email', '')
        
    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(MyRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(MyRegistrationForm, self).clean()

        # test the google recaptcha
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': self.request.POST.get(u'g-recaptcha-response', None),
            'remoteip': self.request.META.get("REMOTE_ADDR", None),
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())

        # result["success"] will be True on a success
        if not result["success"]:
            raise forms.ValidationError(_(u'Only humans are allowed to submit this form.'))

        return self.cleaned_data

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.firstname = self.cleaned_data['first_name']
        user.lastname = self.cleaned_data['last_name']

        if commit:
            user.save()
            
        return user


class MyDetailForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('image','description')


class MatchForm(forms.Form):
    key = forms.CharField(label='User Key', max_length=100)                


