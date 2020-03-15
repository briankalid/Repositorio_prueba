import twitter
import tweepy
from tweepy import OAuthHandler
from datetime import date

#Insert your keys
consumer_key = <insert your consumer_key>
consumer_secret = <insert your consumer_secret>
access_token = <insert your access_token>
access_secret = <insert you access_secret>

# ID of Mexico in twitter trends
MX_WOE_ID = 23424900

# Access with library twitter
auth = twitter.oauth.OAuth(access_token,access_secret,consumer_key,consumer_secret)
api = twitter.Twitter(auth=auth)

# We get trends in Mexico and print
mx_trends = api.trends.place(_id=MX_WOE_ID)

print("Trending in Mexico:")

tendencias=[]
for elemento in mx_trends:
    for dic in elemento["trends"]:
        tendencias.append(dic["name"])
        print(dic["name"])


# Access with library tweepy
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)


# We collect today's popular tweets for each trend and print
date_since = date.today()
for tendencia in tendencias:
    print("---------------------",tendencia,"------------------------------")
    tweets=tweepy.Cursor(api.search,q=tendencia,lang="es",result_type="popular",since=date_since).items()
    for tweet in tweets:
        print(tweet.text,tweet.created_at,"Hashtags:",tweet.entities["hashtags"])
