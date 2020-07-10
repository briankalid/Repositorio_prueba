from flask_mysqldb import MySQL
# from flask import Flask, render_template
import secret

def init_bd(app):
    app.config['MYSQL_HOST'] = secret.host_db()
    app.config['MYSQL_USER'] = secret.user_db()
    app.config['MYSQL_PASSWORD'] = secret.password_db()
    app.config['MYSQL_DB'] = secret.name_db()

    mysql = MySQL(app)
    return(mysql)
