# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0005_t_hashtag_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_HashFriends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_hash', models.ForeignKey(related_name=b'base', to='miner.T_Hashtag')),
                ('related_hash', models.ForeignKey(related_name=b'related', to='miner.T_Hashtag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='t_hashtag',
            name='friends',
        ),
    ]
