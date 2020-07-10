import twitter
import tweepy
from tweepy import OAuthHandler
from datetime import date
import secret
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
    tendencias=[]
    for elemento in mx_trends:
        for dic in elemento["trends"]:
            tendencias.append(dic["name"])
    return tendencias



def obtain_publications(trending):
    # Access with library tweepy
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)
    # We collect today's popular tweets for each trend and print
    tweets_list=[]
    for trend in trending:
        # print("---------------------",tre,"------------------------------")
        tweets=tweepy.Cursor(api.search,q=trend,lang="es",result_type="popular").items()
        tweets_list.append(tweets)
    return tweets_list
