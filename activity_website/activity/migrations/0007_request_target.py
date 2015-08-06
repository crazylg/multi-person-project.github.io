# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='target',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
