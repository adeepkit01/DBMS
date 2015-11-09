# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name=b'Active')),
                ('name', models.CharField(max_length=128, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Description')),
                ('image', models.ImageField(upload_to=b'items/', null=True, verbose_name=b'Image', blank=True)),
                ('added_on', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Added on', editable=False)),
                ('last_modified', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified on', editable=False)),
                ('rented_on', models.DateTimeField(null=True, verbose_name=b'Rented on', blank=True)),
                ('rented_to', models.DateTimeField(null=True, verbose_name=b'Rented to', blank=True)),
                ('rent_power', models.SmallIntegerField(default=50, help_text='Power needed to rent item.', verbose_name=b'Rent Power')),
                ('vision_power', models.SmallIntegerField(default=50, help_text='Power needed to view item.', verbose_name=b'Vision Power')),
                ('price', models.IntegerField(null=True, blank=True)),
                ('added_by', models.ForeignKey(related_name='items_added', verbose_name=b'Added by', to=settings.AUTH_USER_MODEL)),
                ('rented_by', models.ForeignKey(related_name='items_rented', verbose_name=b'Rented by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-added_on', '-last_modified'],
                'get_latest_by': 'added_on',
            },
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(verbose_name=b'Slug')),
            ],
        ),
        migrations.AddField(
            model_name='subscription',
            name='subTag',
            field=models.ForeignKey(to='items.Tag'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subuser',
            field=models.ForeignKey(related_name='subscription_user', verbose_name=b'Subscription User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='items.Tag', verbose_name=b'Tag'),
        ),
    ]
