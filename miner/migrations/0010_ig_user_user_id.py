# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0009_auto_20141003_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='ig_user',
            name='user_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
