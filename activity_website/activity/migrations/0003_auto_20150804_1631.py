# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_request_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='members',
            field=models.ManyToManyField(related_name='activity_member', to='activity.User'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='organizer',
            field=models.ForeignKey(related_name='activity_organizer', to='activity.User'),
        ),
    ]
