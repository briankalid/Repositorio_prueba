from mysql.connector import errorcode
import mysql.connector
import json
import pickle
import re

def create_urls(user,id_u):
    return("https://twitter.com/"+user+"/status/"+id_u)

def update(trending,publications):
    with open('db.json') as json_file:
        config = json.load(json_file)
        json_file.close()

    try:
        cnx = mysql.connector.connect(**config)
        print('\n'+'\033[0;32m'+'Conexion a la base de datos exitosa'+'\033[0;m')
        cursor = cnx.cursor()

        for trend in range(len(trending)):
            for publication in publications[trend]:
                # publication = json.load(publication)
                # print(publication)
                print('\033[0;34m'+trending[trend],'\033[0;37m'+'====','\033[0;m'+publication['text'])
                Trend = trending[trend]
                User = publication['user']['screen_name']
                id_str = publication['id_str']
                URL = create_urls(User,id_str)
                Followers = publication['user']['followers_count']
                Verified = publication['user']['verified']

                if Verified:
                    Verified = 1
                else:
                    Verified = 0

                Retweets = publication['retweet_count']
                Favorite = publication['favorite_count']
                Source = publication['source']

                # for i in range(len(Source)):
                keyword = '"nofollow">'
                before_keyword, keyword, after_keyword = Source.partition(keyword)
                Source = after_keyword.rstrip('</a>')

                print(Source)

                try:
                    query = ("""INSERT INTO publications (id,trend,user,url_pub,followers_count,verified,retweet_count,favorite_count,source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
                    cursor.execute(query,(id_str,Trend,User,URL,Followers,Verified,Retweets,Favorite,Source))
                    cnx.commit()
                    print('\033[0;32m'+'This record was uploaded'+'\n')
                except (mysql.connector.Error,mysql.connector.Warning) as e:
                    print('\033[0;31m'+str(e)+'\n')
                    pass
        print('\033[0;32m'+'Database update completed'+'\n'+'\033[0;m')

        cnx.close()
        cursor.close()
        return(trending,publications)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


publications = []
with open('tweets.pickle','rb') as file:
    publications=pickle.load(file)
    file.close()

trending = []
with open('trending.dat','r') as file:
    for line in file:
        trending.append(line[:-1])
    file.close()

update(trending,publications)
