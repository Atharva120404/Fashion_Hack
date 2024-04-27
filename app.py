from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = 'test'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

app.run(debug=True)
