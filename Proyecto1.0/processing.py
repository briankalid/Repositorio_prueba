from mysql.connector import errorcode
import mysql.connector
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date
import update_local_data

seguidores=[]
verificado=[]
num_retweets=[]
num_favorites=[]
idd=[]
handler=[]
sources=[]


def query_data_base():
    with open('db.json') as json_file:
        config = json.load(json_file)
        json_file.close()

    try:
        cnx = mysql.connector.connect(**config)
        print('\n'+'\033[0;32m'+'Conexion a la base de datos exitosa'+'\033[0;m')
        cursor = cnx.cursor()
        try:
            for trend in trending:
                query = "SELECT * FROM publications WHERE trend = '%s'" %trend
                cursor.execute(query)
                data = cursor.fetchall()
                publications.append(data)
        except (mysql.connector.Error,mysql.connector.Warning) as e:
            print('\033[0;31m'+str(e)+'\n'+'\033[0;m')
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


def create_urls(user,id_u):
    return("https://twitter.com/"+user+"/status/"+id_u)

def main():
    #Here we get the data that we need from the json file

    for trend in publications:
        for publication in trend:
            if len(publication)>0:
                idd.append(publication[0])
                num_retweets.append(int(publication[6]))
                num_favorites.append(int(publication[7]))
                handler.append(publication[2])
                seguidores.append(int(publication[4]))
                verificado.append(publication[5])
                sources.append(publication[8])


    rt_sorted=(sorted(num_retweets))
    mean_of_retweets=np.mean(num_retweets)
    favs_sorted=(sorted(num_favorites))
    mean_of_favs=np.mean(num_favorites)

    #That data that we got, now we pass it to a dataframe for better analysis
    df = pd.DataFrame(idd)
    df.rename(columns={0:'Tweet id'}, inplace=True)
    df['User'] = handler
    df['Verified'] = verificado
    df['Followers'] = seguidores
    df['Retweets'] = num_retweets
    df['Favorites'] = num_favorites
    # df['Date'] = fecha
    sum_interactions = df["Retweets"] + df["Favorites"]




    #Here we obtain the most popular tweet based on the number of favorites and retweets
    df["Sum of interactions"] = sum_interactions


    top=df.sort_values(['Sum of interactions'],ascending=False).head(10)
    urls = create_urls(top['User'],top['Tweet id'])
    top_dat= open('data/top_url.dat','w')
    for url in urls:
        top_dat.write(str(url)+'\n')
    top_dat.close()



    maxxx=df.loc[df['Sum of interactions'].idxmax()]
    id_max=maxxx['Tweet id']
    rts=maxxx['Retweets']
    favs=maxxx['Favorites']
    handlermax=maxxx['User']
    followmax=maxxx['Followers']
    followval = followmax.item()
    rtsval = rts.item()
    favsval = favs.item()

    print(maxxx,"\n")

    print('User','@',handlermax)
    print('Number of followers:',followval)
    print('Tweet id:',id_max)
    print('Number of retweets:',rts)
    print('Number of favorites:',favs)


    create_graphic_retweets(rt_sorted,mean_of_retweets,favs_sorted,mean_of_favs)
    create_graphic_favs(rt_sorted,mean_of_retweets,favs_sorted,mean_of_favs)
    create_graphic_sources()

    followerstr=str(followval)
    rtsstr=str(rtsval)
    favstr=str(favsval)

    update_local_data.update_data(followerstr,rtsstr,favstr)

    create_graphic_favsandrts()
    create_graphic_follow()



def create_graphic_retweets(rt_sorted,mean_of_retweets,favs_sorted,mean_of_favs):
    #Plot of the retweets
    plt.figure()
    x = np.arange(len(num_retweets))
    y = np.array(num_retweets)
    x1=np.arange(len(num_retweets))
    y1=np.array(rt_sorted)
    plt.subplot(211)
    plt.plot(x, y,'x', label='Retweets',color='red')
    plt.axhline(y=mean_of_retweets, color='green', linestyle='-',label='Mean')
    plt.legend()
    plt.subplot(212)
    plt.plot(x1, y1,'.', label='Retweets sorted')
    plt.axhline(y=mean_of_retweets, color='green', linestyle='-',label='Mean')
    plt.legend()
    plt.savefig('static/img/retweets.png')
    plt.close()

def create_graphic_favs(rt_sorted,mean_of_retweets,favs_sorted,mean_of_favs):

    #Plot of the favs
    plt.figure()
    xfav = np.arange(len(num_favorites))
    yfav = np.array(num_favorites)
    xfavsorted=np.arange(len(num_favorites))
    yfavsorted=np.array(favs_sorted)
    plt.subplot(211)
    plt.plot(xfav, yfav,'x', label='Favorites',color='red')
    plt.axhline(y=mean_of_favs, color='green', linestyle='-',label='Mean')
    plt.legend()
    plt.subplot(212)
    plt.plot(xfavsorted, yfavsorted,'.', label='Favorites sorted')
    plt.axhline(y=mean_of_favs, color='green', linestyle='-',label='Mean')
    plt.legend()
    plt.savefig('static/img/fav.png')
    plt.close()

def create_graphic_sources():
    values=[]
    keys=list(set(sources))
    for source in keys:
         values.append(sources.count(source))


    fig, ax = plt.subplots(figsize =((10, 8)))
    ax.barh(keys, values,color=(0.1, 0.1, 0.1, 0.1),  edgecolor='blue')
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    ax.grid(b = True, color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.2)
    ax.invert_yaxis()
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                 str(round((i.get_width()), 2)),
                 fontsize = 10, fontweight ='bold',
                 color ='grey')
    ax.set_title('From which source we are obtaining the most popular tweets',
                 loc ='left', )

    plt.savefig('static/img/sources.png')
    plt.close()

def create_graphic_favsandrts():

    with open('data/maxrts.txt', 'r') as f:
        x = f.readlines()
        f.close()

    rts= [s.rstrip() for s in x]

    with open('data/maxfvs.txt', 'r') as f1:
        x1 = f1.readlines()
        f1.close()

    favs= [s.rstrip() for s in x1]

    with open('data/time.txt', 'r') as f3:
        x3 = f3.readlines()
        f3.close()

    date = [s.rstrip() for s in x3]

    for i in range(0,len(rts)):
        rts[i] = int(rts[i])
        favs[i] = int(favs[i])


    plt.figure()
    x = np.arange(len(rts))
    y = np.array(rts)
    x1=np.arange(len(favs))
    y1 = np.array(favs)
    plt.xticks(x,date, rotation=270)
    plt.plot(x, y,label='Retweets',color='blue')
    plt.plot(x1, y1,label='Favorites',color='red')
    plt.suptitle('Comparison of the number of likes and retweets of the tweet with more interactions')
    plt.legend()
    # plt.show()
    plt.savefig('static/img/favsandrts.png')
    plt.close()


def create_graphic_follow():
    with open('data/time.txt', 'r') as f2:
        x2 = f2.readlines()
        f2.close()

    date1 = [s.rstrip() for s in x2]


    with open('data/maxfollow.txt', 'r') as f3:
        x3 = f3.readlines()
        f3.close()

    list_of_max_followers= [s.rstrip() for s in x3]

    for i in range(0,len(list_of_max_followers)):
        list_of_max_followers[i] = int(list_of_max_followers[i])

    plt.figure()
    x = np.arange(len(list_of_max_followers))
    y = np.array(list_of_max_followers)
    plt.subplot(211)
    plt.xticks(x,date1, rotation=90)
    plt.plot(x, y,'.', label='Followers',color='blue')
    plt.suptitle('Number of followers of the tweet with more interactions')
    plt.legend()
    plt.savefig('static/img/follow.png')
    plt.close()


publications=[]
trending = []
with open('trending.dat','r') as file:
    for line in file:
        trending.append(line[:-1])
    file.close()

query_data_base()
main()
