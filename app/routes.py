from flask import jsonify, request
from app import app, model

@app.route('/api/hello', methods=['GET'])
async def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/predict', methods=['POST'])
async def predict_image():
    data = request.json
    image_path = data.get('path')
    result, evaluation = await model.get_result(image_path)

    return jsonify({'result': result}), 200