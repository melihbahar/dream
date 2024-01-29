import os
import pickle
import sys

import pandas as pd
from flask import Flask, request, jsonify

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(module_path)

app = Flask(__name__)

model = pickle.load(open('model/final_model.pickle', 'rb'))
preprocess_pipeline = pickle.load(open('model/preprocess_pipeline.pickle', 'rb'))


@app.route('/info', methods=['GET'])
def info():
    welcome_message: str = 'Welcome to the API!'
    return welcome_message


@app.route('/predict', methods=['POST'])
def predict():
    new_data = request.json

    try:
        new_data_df: pd.DataFrame = pd.DataFrame(new_data)
    except KeyError:
        return jsonify({'error': 'Invalid request'})

    try:
        processed_df: pd.DataFrame = preprocess_pipeline.transform(new_data_df)
    except Exception as e:
        return jsonify({'error': f'Error during preprocessing: {e}'})

    try:
        prediction = model.predict(processed_df)
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': f'Error during prediction: {e}'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
