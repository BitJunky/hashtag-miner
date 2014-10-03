from django.db import models

# Create your models here.

class IG_Hashtag(models.Model):
    name = models.CharField(max_length=200)

class IG_HashFriends(models.Model):
    base_hash = models.ForeignKey(IG_Hashtag,related_name='base')
    related_hash = models.ForeignKey(IG_Hashtag,related_name='related') 

class IG_HashtagRankings(models.Model):
    reference_hashtag = models.ForeignKey(IG_Hashtag,related_name='reference')
    associated_hashtag = models.ForeignKey(IG_Hashtag,related_name='associated')
    score = models.FloatField()

class IG_User(models.Model):
    username = models.CharField(max_length=200)
    rating = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

class IG_Image(models.Model):
    url = models.URLField()
    likes = models.IntegerField()
    user = models.ForeignKey(IG_User)

class IG_ImageTags(models.Model):
    image = models.ForeignKey(IG_Image)
    hashtag = models.ForeignKey(IG_Hashtag)

class T_Hashtag(models.Model):
    name = models.CharField(max_length=200)

class T_HashFriends(models.Model):
    base_hash = models.ForeignKey(T_Hashtag,related_name='base')
    related_hash = models.ForeignKey(T_Hashtag,related_name='related')

class T_User(models.Model):
    name = models.CharField(max_length=200)
    followers = models.IntegerField(null=True)

class T_Tweet(models.Model):
    tweet = models.CharField(max_length=200)
    user = models.ForeignKey(T_User,null=True)
    retweets = models.IntegerField()
    favorited = models.IntegerField()

class T_TweetTags(models.Model):
    tweet = models.ForeignKey(T_Tweet)
    hashtag = models.ForeignKey(T_Hashtag)



