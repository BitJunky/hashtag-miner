from django.db import models

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=200)

class HashtagRankings(models.Model):
    reference_hashtag = models.ForeignKey(Hashtag,related_name='reference')
    associated_hashtag = models.ForeignKey(Hashtag,related_name='associated')
    score = models.FloatField()

class User(models.Model):
    username = models.CharField(max_length=200)
    rating = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

class Image(models.Model):
    url = models.URLField()
    likes = models.IntegerField()
    user = models.ForeignKey(User)
    hashtags = models.ManyToManyField(Hashtag)
