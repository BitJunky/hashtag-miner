import requests
from django.conf import settings
import numpy as np
import pandas as pd
from miner.models import IG_Hashtag,IG_Image,IG_User,IG_ImageTags,IG_HashFriends

class Hashtagerator:

    def __init__(self,access_token,keyword='ebola'):

        self.keyword = keyword
        self.access_token = access_token

    def get_images(self,keyword=None,max_iter=5):

        if keyword is None:
            keyword = self.keyword

        r = requests.get('https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s' % (self.keyword,self.access_token))
        if r.status_code/2 == 100:
            listomages = []
            counter = 0
            while True:    
                counter += 1
                r_json = r.json()
                if 'data' in r_json:
                    listomages += r_json['data']
                    if ('pagination' in r_json) & ('next_url' in r_json['pagination']) & (counter < max_iter):
                        r = requests.get(r_json['pagination']['next_url'])
                        continue
                    else:
                        break
                break

        return listomages

    def count_tags(self,keyword=None):
    
        if keyword is None:
            keyword = self.keyword

        r = requests.get('https://api.instagram.com/v1/tags/search?q=%s&access_token=%s' % (keyword,self.access_token))
        if r.status_code/2 == 100:
            return pd.DataFrame(r.json()['data'])

    def juice_image(self,img):

        hashtags = img['tags']
        user = img['user']['id']
        username = img['user']['username']
        url = img['images']['low_resolution']['url']
        likes = img['likes']['count']
        return {'id':img['id'],'user_id':user,'username':username,'hashtags':hashtags,'url':url,'likes':likes}

    def collate_mages(self,image_dicts):

        hashtags,users = {},[]
        for img in image_dicts:
            users.append(img['user_id'])
            for hashtag in img['hashtags']:
                if hashtag in hashtags:
                    hashtags.update({hashtag:hashtags[hashtag] + [img['id']]})
                else:
                    hashtags[hashtag] = [img['id']]

        return hashtags,set(users)

    def get_user(self,user_id,max_iter=2):

        r_mages = requests.get('https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s' % (user_id,self.access_token))
        r_user = requests.get('https://api.instagram.com/v1/users/%s/?access_token=%s' % (user_id,self.access_token))
        if r_user.status_code/2 == 100:
            user_details = r_user.json()['data']
#            mages = []
#            counter = 0
#            print user_id
#            while True:
#                counter += 1
#                r_json = r_mages.json()
#                if ('data' in r_json):
#                    mages += [img['likes']['count'] for img in r_json['data']]
#                    if ('pagination' in r_json) & ('next_url' in r_json['pagination']) & (counter<max_iter):
#                        r = requests.get(r_json['pagination']['next_url'])
#                        continue
#                    else:
#                        break
#                break
#
#            user_details['avg_likes'] = np.mean(mages)
            return user_details
                                        
 

    def score_related_hashtags(self,keyword):
        images = self.get_images(keyword,max_iter=10)   
        img_info = [self.juice_image(img) for img in images]
        hashtags, users = self.collate_mages(img_info)
        user_info = {user: self.get_user(user) for user in users}

        img_df = pd.DataFrame(img_info)
        img_df['user_avg'] = [user_info[row.user_id]['avg_likes'] for ii,row in img_df.iterrows()]
        img_df['user_followers'] = [user_info[row.user_id]['counts']['followed_by'] for ii,row in img_df.iterrows()]
        img_df = img_df.set_index('id')

        hashtag_scores = {}
        for hashtag,imgs in hashtags.iteritems():
            scores,weights = [],[]
            for img in imgs:
                scores.append( img_df.loc[img]['likes']/img_df.loc[img]['user_avg'])
                weights.append( img_df.loc[img]['user_followers']  )
            score = np.sum((np.array(scores)*np.array(weights)/np.sum(weights)))
            hashtag_scores.update({hashtag:(score,len(imgs))})
        
        return hashtag_scores 

    def store_in_db(self,keyword,max_iters=2):

        keyword = keyword.lower().replace('#','')
        images = self.get_images(keyword,max_iters)
        img_info = [self.juice_image(img) for img in images]
        hashtags, users = self.collate_mages(img_info)
        user_info = {user: self.get_user(user) for user in users}
        
        # create base hashtag
        db_base_tag,created = IG_Hashtag.objects.get_or_create(name = keyword)

        for image in images:
            img_info = self.juice_image(image) 
            user = self.get_user(img_info['user_id'])
        # create users
            IG_User.objects.filter(user_id = img_info['user_id'],username = img_info['username'],rating = user_info[img_info['user_id']]['counts']['followed_by'])
            db_user,user_created = IG_User.objects.get_or_create(user_id = img_info['user_id'],username = img_info['username'],rating = user_info[img_info['user_id']]['counts']['followed_by'])

        # create image
            db_image,created = IG_Image.objects.get_or_create(IG_id=img_info['id'],url=img_info['url'],likes=img_info['likes'],user = db_user)

        # create other hashtags and friends
            for hashtag in img_info['hashtags']:
                db_tag,created = IG_Hashtag.objects.get_or_create(name=hashtag.lower())
                IG_HashFriends.objects.get_or_create(base_hash=db_base_tag,related_hash=db_tag)
                IG_ImageTags.objects.get_or_create(image = db_image, hashtag = db_tag)
                
        
    def get_top_images(self,hashtag):

        try:
            db_tag = IG_Hashtag.objects.filter(name = hashtag.lower())[0]
        except:
            return None

        QS = IG_ImageTags.objects.filter(hashtag=db_tag)
        Image_URLS = []
        for qs in QS:
            Image_URLS.append((qs.image.url,qs.image.likes,qs.image.user.username))
        return sorted(Image_URLS,key=lambda x: x[1],reverse=True)

    def get_related_tags(self,hashtag):

        try:
            db_tag = IG_Hashtag.objects.filter(name = hashtag.lower())[0]
        except:
            return None

        QS = IG_HashFriends.objects.filter(base_hash=db_tag)
        related_tags = []
        for qs in QS:
            related_tag = qs.related_hash
            if related_tag.name == hashtag:
                continue
            related_mages = IG_ImageTags.objects.filter(hashtag=related_tag)
            sum_likes = np.sum([img.image.likes for img in related_mages])
            related_tags.append((related_tag.name,sum_likes))

        return sorted(related_tags,key=lambda x: x[1],reverse=True)
            
                
                
#    def get_images(self):
#
#
#    def juice_image(self,img):


