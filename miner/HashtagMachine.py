import requests
from django.conf import settings
import numpy as np
import pandas as pd

class Hashtagerator:

    def __init__(self,code,keyword='ebola'):

        self.keyword = keyword
        keys = {'client_id':settings.IG_CLIENT_ID,'client_secret':settings.IG_CLIENT_SECRET,'grant_type':'authorization_code','redirect_uri':settings.IG_REDIRECT,'code':code}
        post = requests.post('https://api.instagram.com/oauth/access_token',data=keys).json()
        self.p = post
        if 'access_token' in post:
            self.authd = True
            self.access_token = post['access_token']
        else:
            self.authd = False

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
        url = img['images']['low_resolution']['url']
        likes = img['likes']['count']
        return {'id':img['id'],'user_id':user,'hashtags':hashtags,'url':url,'likes':likes}

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
            mages = []
            counter = 0
            print user_id
            while True:
                counter += 1
                r_json = r_mages.json()
                if ('data' in r_json):
                    mages += [img['likes']['count'] for img in r_json['data']]
                    if ('pagination' in r_json) & ('next_url' in r_json['pagination']) & (counter<max_iter):
                        r = requests.get(r_json['pagination']['next_url'])
                        continue
                    else:
                        break
                break

            user_details['avg_likes'] = np.mean(mages)
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
        
        

#    def describe_user(self,user_id):




    
            
                
                
#    def get_images(self):
#
#
#    def juice_image(self,img):


