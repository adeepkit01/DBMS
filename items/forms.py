# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.extras.widgets import SelectDateWidget, SelectDateWidget
from items.models import *
from django.conf import settings
from django.utils.translation import ugettext as _
import urllib
import urllib2
import json

class ReserveItem(forms.Form):
    reserve_to = forms.DateTimeField()
    # comment = forms.CharField(label="Komentarz", widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(ReserveItem, self).__init__(*args, **kwargs)

    def clean(self):
        super(ReserveItem, self).clean()

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

class registerForm(forms.Form):
    image = forms.ImageField()

class itemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name','description', 'image', 'tags', 'price')
    
    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(itemForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(itemForm, self).clean()

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

