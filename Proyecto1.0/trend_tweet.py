import twitter
import tweepy
from tweepy import OAuthHandler
from datetime import date
import secret
import json
import pickle
#Insert your keys
consumer_key = secret.consumer_key()
consumer_secret = secret.consumer_secret()
access_token = secret.access_token()
access_secret = secret.access_secret()

# ID of Mexico in twitter trends
MX_WOE_ID = 23424900

# Access with library twitter
def obtain_trends():
    auth = twitter.oauth.OAuth(access_token,access_secret,consumer_key,consumer_secret)
    api = twitter.Twitter(auth=auth)
    # We get trends in Mexico and print
    mx_trends = api.trends.place(_id=MX_WOE_ID)
    trending=[]
    for elemento in mx_trends:
        for dic in elemento["trends"]:
            trending.append(dic["name"])
    # return tendencias[:20]
    with open('trending.dat','w') as file:
        for trend in trending[:30]:
            file.write(trend+'\n')
        file.close()


def obtain_publications():
    # Access with library tweepy
    trending = []
    with open('trending.dat','r') as file:
            for linea in file:
                trending.append(linea[:-1])
            file.close()
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)
    # We collect today's popular tweets for each trend and print
    tweets_list=[]

    for trend in trending:
        tmp=[]
        # print("---------------------",tre,"------------------------------")
        tweets=tweepy.Cursor(api.search,q=trend,lang="es",result_type="popular").items()
        for tweet in tweets:
            tmp.append(tweet._json)
            print(tmp)
        tweets_list.append(tmp)
        with open('tweets.pickle','wb') as file:
            pickle.dump(tweets_list, file)
            file.close()


obtain_trends()
obtain_publications()
