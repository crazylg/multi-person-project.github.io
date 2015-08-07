# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20150807_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headImg',
            field=models.FileField(upload_to='./templates/static/headimg/'),
        ),
    ]
