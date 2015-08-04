# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
