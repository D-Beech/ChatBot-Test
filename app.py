from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

LLAMA_API_URL = "http://localhost:11434/api/generate" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reverse', methods=['POST'])
def reverse():
    data = request.get_json()
    user_message = data.get("message", "")
    print(user_message)
    bot_response = user_message[::-1]  # Reverse the input message
    return jsonify({"response": bot_response})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    payload = {
        "model": "llama3.2",  # Adjust if needed
        "prompt" : user_message,
        "stream" : False
    }

    response = requests.post(LLAMA_API_URL, json=payload, timeout=60)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)