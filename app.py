from flask import Flask, render_template, request, redirect, url_for, session, Response,send_from_directory
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re
import cv2
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from flask import request
import urllib.request 
from PIL import Image 
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.models import Sequential
from numpy.linalg import norm
from sklearn.neighbors import NearestNeighbors
import pickle
from PIL import Image
import random
# Load precomputed features and image file paths
features_list = pickle.load(open(r"C:\Users\Admin\Desktop\Hackathon\image_features_embedding.pkl", "rb"))
img_files_list = pickle.load(open(r"C:\Users\Admin\Desktop\Hackathon\img_files.pkl", "rb"))

# Load pre-trained ResNet50 model
model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
model.trainable = False
model = Sequential([model, GlobalMaxPooling2D()])

app = Flask(__name__)
app.secret_key = 'test'

# clothing_products = [
#     {"product_name": "T-Shirt", "prod_description": "Cotton short-sleeve shirt", "pricing": 15.99},
#     {"product_name": "Jeans", "prod_description": "Denim pants", "pricing": 29.99},
#     {"product_name": "Hoodie", "prod_description": "Fleece pullover hoodie", "pricing": 39.99},
#     {"product_name": "Dress", "prod_description": "Floral print summer dress", "pricing": 49.99},
#     {"product_name": "Jacket", "prod_description": "Waterproof windbreaker jacket", "pricing": 59.99},
#     {"product_name": "Skirt", "prod_description": "A-line denim skirt", "pricing": 24.99},
#     {"product_name": "Sweater", "prod_description": "Knitted wool sweater", "pricing": 34.99},
#     {"product_name": "Shorts", "prod_description": "Cargo shorts with pockets", "pricing": 19.99},
#     {"product_name": "Blouse", "prod_description": "Silk floral print blouse", "pricing": 29.99},
#     {"product_name": "Pants", "prod_description": "Slim-fit chino pants", "pricing": 39.99}
# ]





app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hackathon'
app.config['MYSQL_PORT'] = 3308

styles_red=pd.read_csv(r'C:\Users\Admin\Desktop\Hackathon\Fashion_Hack\combined (1).csv')
# images = pd.read_csv('')
styles_red['productDisplayName'] = styles_red['productDisplayName'].str.lower().str.replace('[^\w\s]', '')
print(styles_red)

# Create a CountVectorizer to convert text to numerical vectors
vectorizer = CountVectorizer()

# Fit and transform the product display names
product_vectors = vectorizer.fit_transform(styles_red['productDisplayName'])

def get_top_n_recommendations(query, n=50):
    # Preprocess the query
    preprocessed_query = query.lower().replace('[^\w\s]', '')

    # Transform the query into a numerical vector
    query_vector = vectorizer.transform([preprocessed_query])

    # Calculate cosine similarity between the query vector and all product vectors
    similarity_scores = cosine_similarity(query_vector, product_vectors)
    print(len(similarity_scores[0]))
    # Get the indices of the top n recommendations
    top_indices = similarity_scores.argsort()[0][-n:][::-1]

    # Return the top n recommendations
    top_recommendations = styles_red.iloc[top_indices] # ['productDisplayName'].tolist()  
    top_rec=top_recommendations.to_dict('records')
    

    return top_rec

def extract_img_features(img, model):
    img_array = image.img_to_array(img)
    expand_img = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expand_img)
    result_to_resnet = model.predict(preprocessed_img)
    flatten_result = result_to_resnet.flatten()
    # Normalizing
    result_normalized = flatten_result / norm(flatten_result)
    return result_normalized

# Define function to recommend similar images
def recommend(features, features_list):
    neighbors = NearestNeighbors(n_neighbors=25, algorithm='brute', metric='euclidean')
    neighbors.fit(features_list)
    distances, indices = neighbors.kneighbors([features])
    return indices

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

@app.route('/shop-details.html')
def shop_details():
     # Retrieve values from the URL query parameters
    link = request.args.get('link')
    article_type = request.args.get('articleType')
    product_display_name = request.args.get('productDisplayName')
    price = request.args.get('price')

    # Create a list to store the values
    product_info = {
        'link': link,
        'article_type': article_type,
        'product_display_name': product_display_name,
        'price': price
    }
    url = link 
    urllib.request.urlretrieve(url, "test.jpg")
    target_image_path = r"C:\Users\Admin\Desktop\Hackathon\test.jpg"
    target_image = Image.open(target_image_path)
    target_image = target_image.resize((224, 224))  # Resize to match the model input size
    target_features = extract_img_features(target_image, model)

    # Get indices of similar images
    similar_image_indices = recommend(target_features, features_list)[0]

    # Display recommended images
    print("Recommended Images:")
    id_list = []
    for i, idx in enumerate(similar_image_indices):
        print(f"{i+1}. {img_files_list[idx]}")
        id = str(img_files_list[idx])
        id = int(id[45:-4])
        id_list.append(id)
    print(id_list)
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # cursor.execute("SELECT (id, subCategory, productDisplayName, price) FROM sty WHERE id = 19834")
    # product_info1 = cursor.fetchall()
    specific_id = 19834  # Change this to the specific ID you want to fetch data for
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    rec_prod_list=[]
    for i in id_list:
        if len(rec_prod_list) >= 5:
            break
        specific_id=i
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT id, subCategory, productDisplayName, price FROM sty WHERE id = %s"
        cursor.execute(query, (specific_id,))
        product_info1 = cursor.fetchone()
        if product_info1 is not None:
            rec_prod_list.append(product_info1)
    count=0
    for i in rec_prod_list:
        file_name=str(i['id'])+'.jpg'
        print(file_name)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT link FROM images WHERE filename = %s"
        cursor.execute(query, (file_name,))
        product_info2 = cursor.fetchone()
        print(product_info2)
        rec_prod_list[count]['link']=product_info2['link']
        count+=1


    print(rec_prod_list)
    




    # Pass the list to the rendered template
    return render_template('shop-details.html', product_info=product_info,rec_prod_list=rec_prod_list,)
    # link = request.args.get('link')
    # article_type = request.args.get('articleType')
    # product_display_name = request.args.get('productDisplayName')
    # season = request.args.get('season')
    # print("Values",link,article_type,product_display_name,season)

    # # Pass these values to your template for rendering
    # return render_template('shop-details.html', links=link, article_type=article_type, product_display_name=product_display_name, season=season)

@app.route("/shop.html",methods=['GET','POST'])
def shop():
     # Retrieve values from the URL query parameters
    link = request.args.get('link')
    article_type = request.args.get('articleType')
    product_display_name = request.args.get('productDisplayName')
    price = request.args.get('price')

    # Create a list to store the values
    list = {
        'link': link,
        'article_type': article_type,
        'product_display_name': product_display_name,
        'price': price
    }
    
    if 'search_box' in request.form:
        search_text = request.form['search_box']
            
        top_rec=get_top_n_recommendations(search_text)
        price_list=[]
        for i in range(len(top_rec)):
            price_list.append(random.randint(500,5000))
            

    print(list)
            

    return render_template('shop.html',lists=top_rec,list=list,price_list=price_list)



@app.route('/shop_women.html')
def shop_women():
    
    combined_data_list = []
    
    # Fetch data from MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT sty.id, sty.subCategory, sty.productDisplayName, sty.price, images.link FROM sty INNER JOIN images ON sty.id = images.filename WHERE sty.gender = 'Women' LIMIT 20;")
    
    for row in cursor.fetchall():
        combined_data_list.append(row)
    
    return render_template('shop_women.html', data=combined_data_list)



@app.route('/shop_men.html')
def shop_men():
    combined_data_list = []
    
    # Fetch data from MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT sty.id, sty.subCategory, sty.productDisplayName, sty.price, images.link FROM sty INNER JOIN images ON sty.id = images.filename WHERE sty.gender = 'Men' LIMIT 20;")
    
    for row in cursor.fetchall():
        combined_data_list.append(row)
    print(combined_data_list)
    return render_template('shop_men.html', data=combined_data_list)
    
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


