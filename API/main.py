from flask import Flask, jsonify
from llmHelpers import generate_response
from flask import request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

@app.route('/response', methods=['POST'])
@cross_origin()

def response():
    data = request.get_json()
    previous_chat = data.get("previous_chat", []) if data else []
    model = data.get("model", "") if data else ""
    return jsonify({"response": generate_response(previous_chat, model)})

if __name__ == '__main__':
    app.run(debug=True)