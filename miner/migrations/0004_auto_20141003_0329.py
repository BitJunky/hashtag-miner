# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0003_auto_20141003_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_user',
            name='followers',
            field=models.IntegerField(null=True),
        ),
    ]
