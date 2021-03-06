from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from items.models import *
from items import forms
from items.forms import *
from django.core.mail import EmailMessage

# @login_required(login_url='/admin')
def index(request):
    user = request.user
    # If user is logged in and it's not anonymous get items with his vision power.
    if not user.is_anonymous and user.userprofile:
        items = Item.objects.filter(active=True, vision_power__lte=user.userprofile.vision_power)
    else:
        items = Item.published.all()
        tags = Tag.objects.all()
    context = {
        'items': items,
        'tags': tags,
    }
    return render(request, 'items/index.html', context)

def indexprice(request):
    user = request.user
    # If user is logged in and it's not anonymous get items with his vision power.
    if not user.is_anonymous and user.userprofile:
        items = Item.objects.filter(active=True, vision_power__lte=user.userprofile.vision_power).order_by('price')
    else:
        items = Item.published.all().order_by('price')
        tags = Tag.objects.all()
    context = {
        'items': items,
        'tags': tags,
    }
    return render(request, 'items/index.html', context)

def indexpriced(request):
    user = request.user
    # If user is logged in and it's not anonymous get items with his vision power.
    if not user.is_anonymous and user.userprofile:
        items = Item.objects.filter(active=True, vision_power__lte=user.userprofile.vision_power).order_by('-price')
    else:
        items = Item.published.all().order_by('-price')
        tags = Tag.objects.all()
    context = {
        'items': items,
        'tags': tags,
    }
    return render(request, 'items/index.html', context)


def subs(request, tag_id):
    user = request.user
    tagw = Tag.objects.get(pk=tag_id)
    sub = subscription(subuser=user, subTag=tagw)
    sub.save()
    messages.success(request, 'Subscription Acknowledged.')
    return HttpResponseRedirect('/')

def unsub(request, tag_id):
    user = request.user
    sub = subscription.objects.filter(subuser=user)
    tagw = Tag.objects.get(pk=tag_id)
    sub = sub.get(subTag = tagw)
    sub.delete()
    messages.success(request, 'Unsubscription Acknowledged.')
    return HttpResponseRedirect('/')



def tagview(request, tag_id):
    # If user is logged in and it's not anonymous get items with his vision power.
    tag = Tag.objects.filter(pk=tag_id)
    tagw = Tag.objects.get(pk=tag_id)
    sub = False
    print request.user.is_anonymous()
    if not request.user.is_anonymous():
        user=request.user
        print "here"
        subq = subscription.objects.filter(subuser=user)
        if subq.filter(subTag=tagw).exists():
            sub = True
    print tagw
    items = Item.objects.filter(tags = tag)
    context = {
        'items': items,
        'tags': tagw,
        'sub' : sub
    }
    return render(request, 'items/tag.html', context)


def view_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
    except (Item.DoesNotExist, Item.MultipleObjectsReturned):
        raise Http404()

    context = {}


    # Check if user have expected vision power
    if item.vision_power > settings.VISION_POWER:
        if request.user.userprofile and item.vision_power <= request.user.userprofile:
                context['item'] = item
        else:
            context['error'] = "You don't have permission to view this item."
    else:
        context['item'] = item

    return render(request, 'items/view.html', context)


def reserve_item(request, item_id):
    print request.method
    if request.method == 'POST' and request.user:
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404()
        user = request.user.userprofile
        form = ReserveItem(request.POST, request=request)
        if form.is_valid():
            print form
            print form.cleaned_data
            form=form.cleaned_data
            item.rented_on=datetime.datetime.now
            print request.user.email
            print item.added_by.email
            user.rent_item(item, form['reserve_to'])
            delta = item.rented_to-item.rented_on
            print delta
            email = EmailMessage('Rent Everything Team', 'Your item '+item.name+' is being rented by '+item.rented_by.username+' (email: '+item.rented_by.email+') for '+str(delta.days)+' days\n Thank you', to=[item.added_by.email])
            email.send()
            email = EmailMessage('Rent Everything Team', 'You are renting item '+item.name+' added by '+item.added_by.username+' (email: '+item.added_by.email+') for '+str(delta.days)+'days at Rs '+str(item.price)+' per day, net amount: Rs '+str(delta.days*item.price)+'. \n Thank you', to=[item.rented_by.email])
            email.send()
            return HttpResponseRedirect('/item/'+item_id+'/')
        else:
            messages.error(request, 'Something went wrong')
            return HttpResponseRedirect('/')

    else:
        if request.user.is_anonymous():
            messages.error(request, 'You need to be logged in')
            return HttpResponseRedirect('/')
        form = ReserveItem()
        try:
            item = Item.objects.get(pk=item_id)
        except (Item.DoesNotExist, Item.MultipleObjectsReturned):
                raise Http404()

        context = {
            'item': item,
            'form': form
        }
        return render(request, 'items/reserve.html', context)

def upload(request):
    if request.method == 'POST':
        form = itemForm(request.POST, request.FILES,request=request)
        if form.is_valid():
            newitem=form.save(commit=False)
            newitem.added_by=request.user
            newitem.save()
            form.save_m2m()
            """for s in subs:
            email = EmailMessage('We have something for you', 'Hey User, we have something special for you in our inventory', to=[subs.subuser.email])
            email.send()"""
            form = form.cleaned_data
            subs = subscription.objects.filter(subTag=form['tags'])
            use = subs.values('subuser')
            for user in use:
                us = User.objects.get(pk=user['subuser'])
                print us.email
                email = EmailMessage('Rent Everything Team', 'We have a new item for you '+form['name']+'. Do check it out at our site.', to=[us.email])
                email.send()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Something went wrong')
            return HttpResponseRedirect('/')
        
    args = {}
    
    args['form'] = itemForm()
    return render(request, 'items/upload.html', args)
