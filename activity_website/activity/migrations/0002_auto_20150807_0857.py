# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='act',
            field=models.ForeignKey(related_name='comment_act', null=True, to='activity.Activity'),
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='poster',
            field=models.ForeignKey(related_name='comment_poster', null=True, to='activity.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
