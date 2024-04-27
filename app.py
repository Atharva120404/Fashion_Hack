from flask import Flask, render_template, request, redirect, url_for, session, Response,send_from_directory
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import cv2
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'test'

print("Atharvba ")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/blog-details.html")
def blog_details():
    return render_template("blog-details.html")

@app.route("/blog.html")
def blog():
    return render_template("blog.html")

@app.route("/checkout.html")
def checkout():
    return render_template("checkout.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/shop-details.html")
def shop_details():
    return render_template("shop-details.html")

@app.route("/shop.html")
def shop():
    return render_template("shop.html")

@app.route("/shopping-cart.html")
def shopping_cart():
    return render_template("shop-cart.html")


if __name__=='__main__':
    app.run(debug=True)


