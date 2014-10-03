from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render   
from miner.HashtagMachine import Hashtagerator as ig_ht 
from miner.twitminer import TwitHasher as twit_ht
from miner.models import IG_HashFriends,T_HashFriends,T_Hashtag,IG_Hashtag
import requests

redirect_uri = 'http://localhost:8000/redirect/'
def index(request):
    if 'access_token' in request.session:
        if request.method == 'POST': 

            hashtag = request.POST.get('hashtag')

            IG = False
            
            if IG == True:
                # check if hash exists
                tt = twit_ht()
                try:
                    db_tag = T_Hashtag.objects.filter(name = hashtag.lower())[0]
                except IndexError:
                    pass
#tt.store_in_db(keyword = hashtag,max_iters=3,no_stream=True)

                # get twitter users,hashtags
                t_users = tt.get_users(hashtag=hashtag)
                t_tags = tt.related_tags(hashtag=hashtag)
                t_tweets = tt.top_tweets(hashtag=hashtag,max_tweets=10)

                context = {'t_users':t_users,'t_tags':t_tags,'t_tweets':t_tweets}

                return HttpResponse('hi')
#return render(request,"miner/t_results.html",context)
            else:  # do IG
                hh = ig_ht()
                try:
                    db_tag = IG_Hashtag.objects.filter(name = hashtag.lower())[0]
                except IndexError:
                    pass
#hh.store_in_db(keyword = hashtag,max_iters=3)

                ig_images = hh.get_top_images(hashtag=hashtag)
                ig_tags = hh.get_related_tags(hashtag=hashtag)
                
                context = {'ig_images':t_images,'ig_tags':ig_tags}
                return HttpResponse('IG')
#                return render(request,"miner/ig_results.html",context)
        else: 
        #display message 
            context = {}
            return render(request,"miner/search.html")
    else:
        IGauth = 'https://api.instagram.com/oauth/authorize/?response_type=code&client_id=%s&redirect_uri=%s' % (settings.IG_CLIENT_ID,redirect_uri)

        return HttpResponseRedirect(IGauth)

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")


def authorize(request):
    code = request.GET.get("code")
    keys = {'client_id':settings.IG_CLIENT_ID,'client_secret':settings.IG_CLIENT_SECRET,'grant_type':'authorization_code','redirect_uri':redirect_uri,'code':code }   
    p = requests.post('https://api.instagram.com/oauth/access_token',data=keys)
    candidate_token = p.json()['access_token']
    request.session['access_token'] = candidate_token
    
    return HttpResponseRedirect('http://localhost:8000/?access_token=%s' % candidate_token)
    
