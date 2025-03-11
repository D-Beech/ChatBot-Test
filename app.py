from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print(user_message)
    bot_response = user_message[::-1]  # Reverse the input message
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)