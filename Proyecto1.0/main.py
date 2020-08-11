import trend_tweet
import update_database
import json
import copy
import processing


trending = trend_tweet.obtain_trends()
print(trending)
publications = trend_tweet.obtain_publications(trending)

trending2 = copy.deepcopy(trending)
publications2 = copy.deepcopy(publications)

with open('trending.dat','w') as file:
    for trend in trending:
        file.write(trend+'\n')
    file.close()

update_database.update(trending,publications)

processing.main(trending2,publications2)
