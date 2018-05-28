import tweepy
import requests
import json
import pandas as pd
import app.models as models
from django.views import generic
from django.shortcuts import render

listing = "https://api.coinmarketcap.com/v2/listings/"

request = requests.get(listing)

#Getting list of top5 coin

data = request.json()['data'][:5]
x = []
for coinn in data:    
    v = coinn['name']
    x.append(v)

#Twitter Token
auth = tweepy.OAuthHandler("Clw72hQFdPE3aELllj4ztTNDq", "XaRFf3cA3c2vPk8nKS0g1E72oDFxl3t872UFaoKhyLQwYoRcBg")
auth.set_access_token("3006444815-zZ4BqQOdTrPpBpBZLJjawtJTo789Pq3feZR8oFc", "MF6HMjsYQ6HZwVklOxC0fIQwwTfk04Cr9MXnWhxLfZnpa")

api = tweepy.API(auth)
results = {}
#x=['Bitcoin', 'Litecoin','Namecoin']
for coin in x:
    value_results=[]
    for tweet in tweepy.Cursor(api.search, q=coin).items(5):
        value_results.append(tweet)
        results[coin]=value_results

final_results = {}  

# processing results and save them in the dataBase    
def process_results():
    for key, value in results.items():
            
        id_list = value
        data_set = pd.DataFrame(id_list)


        data_set["retweet_count"] = [tweet.retweet_count for tweet in id_list]
        data_set["user_followers_count"] = [tweet.author.followers_count for tweet in id_list]
        
        res = final_results[key]= {}
        retweet_sum= data_set["retweet_count"].sum()
        followers_sum= data_set["user_followers_count"].sum()
        res['retweet_sum'] = retweet_sum
        res['followers_sum'] = followers_sum
    for key, value in final_results.items():
        record = models.results.objects.create(coin=key, retweets=value["retweet_sum"], followers=value["followers_sum"])
        record.save()

process_results()
print('created')

#Displaying the results
class indexView(generic.ListView):
    model = models.results
    template_name = 'table.html'