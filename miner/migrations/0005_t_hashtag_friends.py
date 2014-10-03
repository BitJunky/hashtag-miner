# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0004_auto_20141003_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_hashtag',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='miner.T_Hashtag'),
            preserve_default=True,
        ),
    ]
