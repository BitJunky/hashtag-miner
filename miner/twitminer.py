from django.conf import settings
import time
import numpy as np
import pandas as pd
import twitter
from miner.models import T_Hashtag,T_Tweet,T_User,T_TweetTags,T_HashFriends
import IPython
from collections import Counter
from twitter import TwitterError
import hashlib
import django.utils.encoding as uu

class TwitHasher:

    def __init__(self):
        
        self.api = twitter.Api(consumer_key=settings.TW_KEY,consumer_secret=settings.TW_SECRET,access_token_key=settings.TW_OAUTH_TOKEN,access_token_secret=settings.TW_OAUTH_SECRET)

    def extract_hashtags(self,tweets,current_tweets):
        hashtags = []
        for tweet in tweets:
            hashed_tweet = hashlib.sha1((tweet.text).encode('utf-8'))
            if hashed_tweet not in current_tweets:
                current_tweets[hashed_tweet] = tweet.text  
                for ht in tweet.hashtags:
                    hashtags.append(ht.text.encode('utf-8').lower())
        return hashtags,current_tweets

    def get_hashtags(self,keyword='ebola',max_iters=10):

        current_tweets = {}
        keyword = keyword.replace('#','')
        pop_tweets = self.api.GetSearch('#'+keyword,count=100)
        hashtags,current_tweets = self.extract_hashtags(pop_tweets,current_tweets)
        counter = 0
        while True:
            counter += 1
            recent_tweets = self.api.GetSearch('#'+keyword,count=100)
            new_hashtags,current_tweets = self.extract_hashtags(recent_tweets,current_tweets)
            old_size = len(hashtags)
            hashtags = hashtags + new_hashtags
            if counter>max_iters:
                break
        return Counter(hashtags) 

    def store_in_db(self,keyword='ebola',max_iters=10,no_stream=True):

        def process_tweets(tweets,base_hashtag):

            for tweet in tweets:
                if tweet.retweeted_status is not None:
                    continue
                try:
                    db_tweet = T_Tweet.objects.get(t_id = tweet.id)
                except T_Tweet.DoesNotExist:
                    db_tweet = T_Tweet.objects.create(t_id = tweet.id,tweet = tweet.text, retweets = tweet.retweet_count, favorited = tweet.favorite_count)
                    created = True
                else:
                    created = False
                if created: #new tweet

                    db_user,user_created = T_User.objects.get_or_create(name = tweet.user.screen_name)
                    db_user.followers = tweet.user.followers_count
                    db_user.save()

                    db_tweet.user = db_user
                    db_tweet.retweets = tweet.retweet_count
                    db_tweet.favorited = tweet.favorite_count
                    db_tweet.save()

                    for hashtag in tweet.hashtags:
                        db_hashtag,created = T_Hashtag.objects.get_or_create(name = hashtag.text.lower())
                        db_tag_tweet = T_TweetTags.objects.create(tweet = db_tweet,hashtag = db_hashtag)
                        T_HashFriends.objects.get_or_create(base_hash=base_hashtag,related_hash=db_hashtag)

        def process_streamed(tweets,base_hashtag):

            for tweet in tweets:
                if 'retweeted_status' in tweet:
                    continue
                try:
                    db_tweet = T_Tweet.objects.get(t_id = tweet['id'])
                except T_Tweet.DoesNotExist:
                    db_tweet = T_Tweet.objects.create(t_id = tweet['id'],tweet = tweet['text'], retweets = tweet['retweet_count'], favorited = tweet['favorite_count'])
                    created = True
                else:
                    created = False

                if created:

                    db_user,user_created = T_User.objects.get_or_create(name = tweet['user']['screen_name'])
                    db_user.followers = tweet['user']['followers_count']
                    db_user.save()
                
                    db_tweet.user = db_user
                    db_tweet.retweets = tweet['retweet_count']
                    db_tweet.favorited = tweet['favorite_count']
                    db_tweet.save()

                    for hashtag in tweet['entities']['hashtags']:
                        db_hashtag,created = T_Hashtag.objects.get_or_create(name = hashtag['text'].lower())
                        db_tag_tweet = T_TweetTags.objects.create(tweet = db_tweet,hashtag = db_hashtag)
                        T_HashFriends.objects.get_or_create(base_hash=base_hashtag,related_hash=db_hashtag)

        keyword = keyword.lower().replace('#','')
        try:
            db_hashtag = T_Hashtag.objects.get(name = keyword)
        except T_Hashtag.DoesNotExist:
            db_hashtag = T_Hashtag.objects.create(name = keyword)   
        pop_tweets = self.api.GetSearch(uu.smart_text('#'+keyword),count=100,result_type='popular')
        if not pop_tweets:
            return None
        
        
        process_tweets(pop_tweets,base_hashtag=db_hashtag)

        counter = 0
        while counter < max_iters:
            try:
                recent_tweets = self.api.GetSearch(uu.smart_text('#'+keyword),count=100,result_type='recent')
            except TwitterError:
                break
            else:
                process_tweets(recent_tweets,base_hashtag=db_hashtag)
                counter += 1
        if not no_stream:
            counter = 0
            recent_tweets = []
            stream = self.api.GetStreamFilter(track=[uu.smart_text('#'+keyword)])
            while counter < max_iters:
                try:
                    tweet = stream.next()
                except (TwitterError,KeyboardInterrupt):
                    break
                else:
                    counter += 1
                    time.sleep(2)
                    recent_tweets.append(tweet)
            process_streamed(recent_tweets,base_hashtag=db_hashtag)

    def get_users(self,hashtag='ebola'):

        try:
            db_hashtag = T_Hashtag.objects.get(name = hashtag.lower())
        except T_Hashtag.DoesNotExit:
            return None

        uses = T_TweetTags.objects.filter(hashtag = db_hashtag)
        users = {}
        for use in uses:
            tweet = use.tweet
            if tweet.user in users:
                users.update({tweet.user: users[tweet.user] + tweet.retweets})
            else:
                users.update({tweet.user:tweet.retweets})
        counts = [(str(user.name),user.followers,retweet) for user,retweet in users.iteritems()]
        return sorted(counts, key=lambda tup: np.log(tup[1])*tup[2],reverse=True)

    def top_tweets(self,hashtag,max_tweets):

        try:
            db_hashtag = T_Hashtag.objects.get(name = hashtag.lower())
        except T_Hashtag.DoesNotExit:
            return None

        counts = []
        uses = T_TweetTags.objects.filter(hashtag = db_hashtag)
        for use in uses:
            counts.append((str(use.tweet.tweet.encode('utf-8')),use.tweet.user.name,use.tweet.retweets))    
        return sorted(counts, key=lambda tup: tup[2],reverse=True)[:max_tweets]


    def related_tags(self,hashtag):

        try:
            db_hashtag = T_Hashtag.objects.get(name = hashtag.lower())
        except T_Hashtag.DoesNotExit:
            return None

        QS = T_HashFriends.objects.filter(base_hash=db_hashtag)
        hash_counts = []
        for qs in QS:
            related_hash = qs.related_hash.name
            if related_hash == hashtag:
                continue
            hash_counts.append((related_hash,self.count_tweets_hash(related_hash),self.count_retweets_hash(related_hash)))
            hash_counts = [hc for hc in hash_counts if hc[0] != 'ebola']

        return sorted(hash_counts, key=lambda tup: tup[1],reverse=True)

    def count_tweets_hash(self,hashtag):

        try:
            db_hashtag = T_Hashtag.objects.get(name = hashtag.lower)
        except T_Hashtag.DoesNotExist:
            return None

        QS = T_TweetTags.objects.filter(hashtag = db_hashtag)
        return len(QS) 

    def count_retweets_hash(self,hashtag):

        try:
            db_hashtag = T_Hashtag.objects.get(name = hashtag.lower)
        except T_Hashtag.DoesNotExist:
            return None

        QS = T_TweetTags.objects.filter(hashtag = db_hashtag)
        retweets = 0
        for qs in QS:
            retweets += qs.tweet.retweets
        return retweets

        
        




        

    
