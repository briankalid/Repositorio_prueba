from mysql.connector import errorcode
import mysql.connector
import json
def create_urls(user,id_u):
    return("https://twitter.com/"+user+"/status/"+id_u)

def update(trending,publications):
    with open('db.json') as json_file:
        config = json.load(json_file)
        json_file.close()

    try:
        cnx = mysql.connector.connect(**config)
        print('Conexion exitosa')
        cursor = cnx.cursor()

        for trend in range(len(trending)):
            for publication in publications[trend]:
                print(trending[trend],'====',publication.text)
                Trend = trending[trend]
                User = publication.user.screen_name
                id_str = publication.id_str
                URL = create_urls(User,id_str)
                Followers = publication.user.followers_count
                Verified = publication.user.verified
                # print('ATENCION!!!!!!!',Verified)
                # print(type(Verified))
                if Verified:
                    Verified = 1
                else:
                    Verified = 0
                # print('ATENCION!!!!!!!',Verified)

                Retweets = publication.retweet_count
                Favorite = publication.favorite_count
                # print(Trend,User,id_str,URL,Followers,Verified,Retweets,Favorite)
                try:
                    query = ("""INSERT INTO publications (trend,user,url_pub,followers_count,verified,retweet_count,favorite_count) VALUES (%s,%s,%s,%s,%s,%s,%s)""")
                    cursor.execute(query,(Trend,User,URL,Followers,Verified,Retweets,Favorite))
                    cnx.commit()
                    print('Se ejecuto la query')
                except:
                    print('No se ejecuto la query')
                    pass


        cnx.close()
        cursor.close()


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
