from flask import jsonify, request
from app import app, model
import random

@app.route('/api/hello', methods=['GET'])
async def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/predict', methods=['POST'])
async def predict_image():
    data = request.json
    image_path = data.get('path')
    result, score = await model.get_result(image_path)

    return jsonify({'result': result, 'score': score}), 200

@app.route('/api/freshness', methods=['POST'])
async def detect_image():
    data = request.json
    image_path = data.get('path')
    # result, score = await model.get_result(image_path)
    list1 = ['Fresh', 'Not Fresh']

    return jsonify({'result': random.choice(list1), 'score': random.random()}), 200

@app.route('/api/toxic', methods=['POST'])
async def predict_text():
    data = request.json
    sentence = [data.get('sentence')]
    result, score = await model.infer(sentence)

    return jsonify({'result': result, 'score': score}), 200