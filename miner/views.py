from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render   
from miner.HashtagMachine import Hashtagerator as ig_ht 
from miner.twitminer import TwitHasher as twit_ht
import requests

redirect_uri = 'http://localhost:8000/redirect/'
def index(request):

    if 'access_token' in request.session:
        if request.method == 'POST': 

            hashtag = request.POST.get('hashtag')

            # get twitter users,hashtags
            tt = twit_ht()
            t_users = tt.get_users(hashtag=hashtag)
            t_tags = tt.related_tags(hashtag=hashtag)

            context = {'t_users':t_users,'t_tags':t_tags}
            return render(request,"miner/results.html",context)
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
    
