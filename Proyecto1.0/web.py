from flask import Flask, render_template, flash
from flask_mysqldb import MySQL
import secret
import database_flask

trending=[]

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
    # print(trending)


@app.route('/')
def home():
    return render_template('graphics.html',trending=trending)


@app.route('/trend/<int:id>')
def trend(id):
    # print('#hola')
    id=trending[id]
    cursor = mysql.connection.cursor()
    query='''SELECT url_pub FROM publications WHERE trend = %s'''
    cursor.execute(query,(id,))
    urls = cursor.fetchall()
    cursor.close()
    print(urls)
    return render_template('Trend.html',urls=urls,trending=trending,trend=id)

if __name__=='__main__':
    app.run(debug=True)
