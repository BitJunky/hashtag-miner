# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IG_HashtagRankings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IG_Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('likes', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='T_Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='T_Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', models.CharField(max_length=200)),
                ('retweets', models.IntegerField()),
                ('favorited', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='T_TweetTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashtag', models.ForeignKey(to='miner.T_Hashtag')),
                ('tweet', models.ForeignKey(to='miner.T_Tweet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='T_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('followers', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Hashtag',
            new_name='IG_Hashtag',
        ),
        migrations.RenameModel(
            old_name='User',
            new_name='IG_User',
        ),
        migrations.RemoveField(
            model_name='hashtagrankings',
            name='associated_hashtag',
        ),
        migrations.RemoveField(
            model_name='hashtagrankings',
            name='reference_hashtag',
        ),
        migrations.DeleteModel(
            name='HashtagRankings',
        ),
        migrations.RemoveField(
            model_name='image',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='t_tweet',
            name='user',
            field=models.ForeignKey(to='miner.T_User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ig_image',
            name='hashtags',
            field=models.ManyToManyField(to='miner.IG_Hashtag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ig_image',
            name='user',
            field=models.ForeignKey(to='miner.IG_User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ig_hashtagrankings',
            name='associated_hashtag',
            field=models.ForeignKey(related_name=b'associated', to='miner.IG_Hashtag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ig_hashtagrankings',
            name='reference_hashtag',
            field=models.ForeignKey(related_name=b'reference', to='miner.IG_Hashtag'),
            preserve_default=True,
        ),
    ]
