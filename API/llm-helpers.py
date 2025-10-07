from flask import Flask, jsonify
from main import generate_response
from flask import request
app = Flask(__name__)

@app.route('/response', methods=['POST'])
def response():
    data = request.get_json()
    previous_chat = data.get("previous_chat", "") if data else ""
    model = data.get("model", "") if data else ""
    return jsonify({"response": generate_response(previous_chat, model)})

if __name__ == '__main__':
    app.run(debug=True)