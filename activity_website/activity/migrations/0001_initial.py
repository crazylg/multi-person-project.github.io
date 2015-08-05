# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('explanation', models.CharField(max_length=400)),
                ('post_time', models.DateTimeField()),
                ('applyend_time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('place', models.CharField(max_length=100)),
                ('min_age', models.PositiveIntegerField()),
                ('max_age', models.PositiveIntegerField()),
                ('sex_requirement', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=100)),
                ('current_size', models.PositiveIntegerField()),
                ('max_size', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('explanation', models.CharField(max_length=400)),
                ('found_time', models.DateTimeField()),
                ('current_size', models.PositiveIntegerField()),
                ('max_size', models.PositiveIntegerField()),
                ('activities', models.ManyToManyField(to='activity.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('content', models.CharField(max_length=500)),
                ('group', models.ForeignKey(related_name='groupmessage_group', to='activity.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=40)),
                ('content', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=100)),
                ('goal', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('account', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=20)),
                ('sex', models.CharField(max_length=10)),
                ('age', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('interest', models.CharField(max_length=200)),
                ('headimg', models.FileField(upload_to='./upload/')),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('content', models.CharField(max_length=500)),
                ('user1', models.ForeignKey(related_name='usermessage_user1', to='activity.User')),
                ('user2', models.ForeignKey(related_name='usermessage_user2', to='activity.User')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='poster',
            field=models.ForeignKey(related_name='request_poster', to='activity.User'),
        ),
        migrations.AddField(
            model_name='request',
            name='receiver',
            field=models.ForeignKey(related_name='request_receiver', to='activity.User'),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='user',
            field=models.ForeignKey(related_name='groupmessage_user', to='activity.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='activity.User', related_name='group_member'),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(related_name='group_owner', to='activity.User'),
        ),
        migrations.AddField(
            model_name='activity',
            name='organizer',
            field=models.ForeignKey(to='activity.User'),
        ),
    ]
