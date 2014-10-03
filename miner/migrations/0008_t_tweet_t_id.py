# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0007_auto_20141003_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_tweet',
            name='t_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
