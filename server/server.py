from flask import Flask, jsonify, request
import os
import base64
import pandas as pd
import json
import sys

app = Flask(__name__)

IMAGE_DIR = 'images'

def load_image_mappings():
    with open('id_category.json', 'r') as f:
        return json.load(f)
id_to_category = load_image_mappings()

def load_image(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Endpoing to find category
@app.route('/category/<image_id>', methods=['GET'])
def get_category(image_id):
    category = id_to_category.get(image_id)
    if category:
        return category
    return None 

# Endpoint to serve images
@app.route('/image/<image_id>', methods=['GET'])
def get_image(image_id):
    category = request.args.get('category', default=None, type=str)
    threshold = request.args.get('threshold', default=None, type=float)
    cached_images = request.args.getlist('cached_images')

    similarity_df = pd.read_csv(os.path.join('images', category, f'{category}.csv'), index_col=0)
    similarities = similarity_df[image_id]
    similarities = similarities[similarities.index.isin(cached_images)]

    similarities = similarities[similarities >= threshold]

    if not similarities.empty:
        best_match = similarities.idxmax()
        return jsonify({"use_cached_image": best_match})

    image_path = os.path.join(IMAGE_DIR, category, f'{image_id}.jpg')
    if os.path.exists(image_path):
        img_data = load_image(image_path)
        return jsonify({"id": image_id, "category": category, "image_data": img_data})
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
