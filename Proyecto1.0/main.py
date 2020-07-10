import trend_tweet
import update_database
# print(trend_tweet.autentic_prue())
trending = trend_tweet.obtain_trends()
print(trending)
publications = trend_tweet.obtain_publications(trending)

with open('trending.dat','w') as file:
    for trend in trending:
        file.write(trend+'\n')
    file.close()

update_database.update(trending,publications)
