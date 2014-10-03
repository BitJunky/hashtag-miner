# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0008_t_tweet_t_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ig_hashtag',
            name='count',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ig_image',
            name='IG_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
