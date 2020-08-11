from flask import Flask, render_template, flash
from flask_mysqldb import MySQL 
import secret
import database_flask
from datetime import date

trending = []
app = Flask(__name__)

mysql = database_flask.init_bd(app)

app.secret_key = secret.app_secret_key()

@app.before_request
def before_request():
    trending.clear()
    with open('trending.dat','r') as file:
        for linea in file:
            trending.append(linea[:-1])
        file.close()


@app.route('/')
def home():
    return render_template('graphics.html',trending=trending,today=date.today().strftime("%d/%m/%Y"))

@app.route('/trend/<int:id>')
def trend(id):
    id=trending[id]
    cursor = mysql.connection.cursor()
    query='''SELECT url_pub FROM publications WHERE trend = %s'''
    cursor.execute(query,(id,))
    urls = cursor.fetchall()
    cursor.close()
    print(urls)
    return render_template('Trend.html',urls=urls,trending=trending,trend=id)

@app.route('/top')
def top():
    top = []
    with open('data/top_url.dat','r') as file:
        for linea in file:
            top.append(linea[:-1])
        file.close()
    print(top)
    return render_template('Top.html',trending=trending,top=top)


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
