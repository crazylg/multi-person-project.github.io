# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20150807_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headImg',
            field=models.FileField(upload_to='./upload/'),
        ),
    ]
