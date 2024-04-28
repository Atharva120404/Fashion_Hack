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

# Load precomputed features and image file paths
features_list = pickle.load(open(r"C:\Users\Admin\Desktop\Hackathon\image_features_embedding.pkl", "rb"))
img_files_list = pickle.load(open(r"C:\Users\Admin\Desktop\Hackathon\img_files.pkl", "rb"))

# Load pre-trained ResNet50 model
model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
model.trainable = False
model = Sequential([model, GlobalMaxPooling2D()])

# Define function to extract image features
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
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    neighbors.fit(features_list)
    distances, indices = neighbors.kneighbors([features])
    return indices

# Load and extract features of the target image
target_image_path = r"C:\Users\Admin\Desktop\Hackathon\10023.jpg"
target_image = Image.open(target_image_path)
target_image = target_image.resize((224, 224))  # Resize to match the model input size
target_features = extract_img_features(target_image, model)

# Get indices of similar images
similar_image_indices = recommend(target_features, features_list)[0]

# Display recommended images
print("Recommended Images:")
for i, idx in enumerate(similar_image_indices):
    print(f"{i+1}. {img_files_list[idx]}")
    # img = Image.open(img_files_list[idx])
    # img.show()
