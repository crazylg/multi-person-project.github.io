# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20150804_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(to='activity.User', related_name='friends_rel_+'),
        ),
    ]
