from flask import Quart, jsonify, request
from models import Predict

predict = Predict()
app = Quart(__name__)

@app.route('/api/hello', methods=['GET'])
async def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/predict', methods=['POST'])
async def predict_image():
    data = await request.json
    image_path = data.get('path')
    result, evaluation = await predict.get_result(image_path)

    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
