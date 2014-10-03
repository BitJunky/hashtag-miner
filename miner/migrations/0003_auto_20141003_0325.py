# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0002_auto_20141003_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_tweet',
            name='user',
            field=models.ForeignKey(to='miner.T_User', null=True),
        ),
    ]
