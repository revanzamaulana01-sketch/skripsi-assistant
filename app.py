from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from inference import InferenceEngine
from validator import Validator
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

engine = InferenceEngine('rules.json')
validator = Validator()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/login.html')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/api/jurusan', methods=['GET'])
def get_jurusan():
    return jsonify({'status': 'success', 'data': engine.get_jurusan_list()})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    is_valid, errors = validator.validate(data)
    if not is_valid:
        return jsonify({'status': 'error', 'errors': errors}), 400
    result = engine.forward_chain(
        data['jurusan'],
        data.get('minat'),
        data.get('metode')
    )
    return jsonify({'status': 'success', 'data': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
