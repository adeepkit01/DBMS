from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User, Group
from profiles.models import UserProfile, GroupProfile
from items.models import subscription
from profiles.forms import *
import random
from django.core.mail import EmailMessage

def view_user(request, user_name):
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        raise Http404()
    sub = subscription.objects.filter(subuser=user)
    context = {
        'user': user,
        'sub' : sub
    }
    return render(request, 'profiles/view_profile.html', context)


def view_group(request, group_id):
    try:
        group = Group.objects.get(pk=group_id)
        group_profile = group.groupprofile
    except Group.DoesNotExist:
        raise Http404()

    context = {
        'group': group,
        'group_profile': group_profile
    }
    return render(request, 'profiles/view_group.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')

    messages.error(request, "Incorrect login credentials.")
    return HttpResponseRedirect('/')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            form=form.cleaned_data
            user = authenticate(username=form['username'], password=form['password1'])
            request.session['user'] = user.pk
            request.session['username'] = form['username']
            request.session['password'] = form['password1']
            n=random.randint(1000,9999)
            request.session['randkey'] = str(n)
            email = EmailMessage('Rent Everything Team', 'Your account creation key is '+str(n)+'. Enter this to procced\nThank you', to=[form['email']])
            email.send()
            print form
            messages.success(request, 'Registration Acknowledged.')
            return HttpResponseRedirect('/verify')
        else:
            messages.error(request, 'Something went wrong')
            return HttpResponseRedirect('/')
        
    args = {}
    
    args['form'] = MyRegistrationForm()
    return render(request, 'profiles/register.html', args)

def detail(request):
    if request.user.is_anonymous():
        messages.error(request, 'You need to be logged in')
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        users = UserProfile(user=request.user)
        users.save()
        form = MyDetailForm(request.POST, request.FILES, instance=users)
        form.save()
        return HttpResponseRedirect('/')
        
    args = {}
    
    args['form'] = MyDetailForm()
    return render(request, 'profiles/fill.html', args)

def verify(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            #print form.cleaned_data
            print form['key']
            print request.session['randkey']
            if form['key']==request.session['randkey']:
                user = authenticate(username=request.session['username'], password=request.session['password'])
                login(request, user)
                return HttpResponseRedirect('/fill')
            else:
                user= User.objects.get(pk=request.session['user'])
                user.delete()
                messages.error(request, 'Wrong Key')
                return HttpResponseRedirect('/')
        
    args = {}
    
    args['form'] = MatchForm()
    return render(request, 'profiles/verify.html', args)
