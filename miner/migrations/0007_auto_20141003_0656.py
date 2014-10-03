# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0006_auto_20141003_0418'),
    ]

    operations = [
        migrations.CreateModel(
            name='IG_HashFriends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_hash', models.ForeignKey(related_name=b'base', to='miner.IG_Hashtag')),
                ('related_hash', models.ForeignKey(related_name=b'related', to='miner.IG_Hashtag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IG_ImageTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashtag', models.ForeignKey(to='miner.IG_Hashtag')),
                ('image', models.ForeignKey(to='miner.IG_Image')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ig_image',
            name='hashtags',
        ),
    ]
