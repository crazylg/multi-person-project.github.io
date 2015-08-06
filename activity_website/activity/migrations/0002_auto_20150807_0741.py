# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='headimg',
        ),
        migrations.AddField(
            model_name='activity',
            name='picture',
            field=models.FileField(null=True, upload_to='./templates/static/act_picture/'),
        ),
        migrations.AddField(
            model_name='user',
            name='headImg',
            field=models.FileField(null=True, upload_to='./templates/static/headimg/'),
        ),
    ]
