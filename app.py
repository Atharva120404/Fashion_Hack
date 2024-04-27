from flask import Flask, render_template, request, redirect, url_for, session, Response,send_from_directory
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re
import cv2
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'test'

clothing_products = [
    {"product_name": "T-Shirt", "prod_description": "Cotton short-sleeve shirt", "pricing": 15.99},
    {"product_name": "Jeans", "prod_description": "Denim pants", "pricing": 29.99},
    {"product_name": "Hoodie", "prod_description": "Fleece pullover hoodie", "pricing": 39.99},
    {"product_name": "Dress", "prod_description": "Floral print summer dress", "pricing": 49.99},
    {"product_name": "Jacket", "prod_description": "Waterproof windbreaker jacket", "pricing": 59.99},
    {"product_name": "Skirt", "prod_description": "A-line denim skirt", "pricing": 24.99},
    {"product_name": "Sweater", "prod_description": "Knitted wool sweater", "pricing": 34.99},
    {"product_name": "Shorts", "prod_description": "Cargo shorts with pockets", "pricing": 19.99},
    {"product_name": "Blouse", "prod_description": "Silk floral print blouse", "pricing": 29.99},
    {"product_name": "Pants", "prod_description": "Slim-fit chino pants", "pricing": 39.99}
]



print("Atharvba ")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hackathon'
app.config['MYSQL_PORT'] = 3308

mysql = MySQL(app)
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inex.html")
def home1():
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

@app.route("/shop.html",methods=['GET','POST'])
def shop():
    return render_template('shop.html',lists=clothing_products)

@app.route('/shop_women.html')
def shop_women():
    combined_data_list = []
    
    # Fetch data from MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT sty.id, sty.subCategory, sty.productDisplayName, sty.price, images.link FROM sty INNER JOIN images ON sty.id = images.filename WHERE sty.gender = 'Women' LIMIT 20;")
    
    for row in cursor.fetchall():
        combined_data_list.append(row)
    
    return render_template('shop_women.html', data=combined_data_list)



    return render_template('shop_women.html', data_list=data_list, data1_list=data1_list)
    
# @app.route('/shop_women.html')
# def shop_women():
#     data_list = []
#     data1_list = []
    
#     # Fetch data from MySQL
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT id,subCategory, productDisplayName, price FROM sty WHERE gender = 'Women'")
    
#     for row in cursor.fetchall():
#         data_list.append(row)
#         id = item['id']
#     input =[]
#     input=data_list[id]
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT link FROM images WHERE id = '%s",(input))
    
#     for row in cursor.fetchall():
#         data1_list.append(row)


    return render_template('shop_women.html', datas=data_list,datas1=data1_list)
    # query = "SELECT * FROM products WHERE category = %s"
    # db_cursor.execute(query, (category,))
    # products = db_cursor.fetchall()
    # product_list = [{'id': product[0], 'name': product[1]} for product in products]
    # return render_template("shop_women.html",lists=clothing_products)
    # #return jsonify(product_list)
    # # cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s', (email, password))
    # # user = cursor.fetchone()
    # return render_template("shop_women.html",lists=clothing_products)

@app.route("/shopping-cart.html")
def shopping_cart():
    return render_template("shopping-cart.html")

@app.route("/product-detail.html?product_id=")
def prod():
    return render_template("shop-details.html")


if __name__=='__main__':
    app.run(debug=True)


